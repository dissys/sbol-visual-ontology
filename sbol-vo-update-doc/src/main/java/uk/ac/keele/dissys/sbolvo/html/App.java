package uk.ac.keele.dissys.sbolvo.html;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

import org.apache.commons.io.FileUtils;
import org.apache.jena.rdf.model.*;
import org.apache.jena.vocabulary.RDFS;
import org.jsoup.*;
import org.jsoup.nodes.*;
import org.jsoup.select.Elements;


/**
 * Hello world!
 *
 */
public class App 
{
	private static String sbolbase="http://sbols.org/visual/v2#";
    /*Steps (Make sure the remote and online Github repo includes the latest sbol.rdf)
     * 1- Remove the sbol-owl-org.htm
     * 2- Take a copy of the LODE from Github: git clone https://github.com/essepuntato/LODE.git
     * 3 - Run LODE:
     * 	cd LODE
     *  mvn clean jetty:run
     *  4 - Save the output from the following URL as sbol-vo.html
     *      http://localhost:8080/lode/extract?url=https://dissys.github.io/sbol-visual-ontology/sbol-vo.rdf
     *  5 - Run this App.java to create the updated sbol-vo.htm with images
     * */
    public static void main( String[] args ) throws IOException
    {
        System.out.print( "..." );
        File source = new File("../sbol-vo.html");
       // File dest = new File("../sbol-vo-org.html");
       //Files.copy(source.toPath(), dest.toPath(),StandardCopyOption.REPLACE_EXISTING);
        
        Document doc = Jsoup.parse(source, "UTF-8");
        //Document doc = Jsoup.parse(new File("../sbol-vo-org.html"), "UTF-8");
        
        cleanHeaders(doc);
       
        Elements links = doc.select("a");
        
        //Remove the localhost links
        for (Element link : links) {
        	String href=link.attr("href");
        	if (href.startsWith("http://localhost"))
        	{
        		href="#" + getAfter(href, "#");
        		link.attr("href",href);
        	}
        	
        	String title=link.attr("title");
        	
        	if (title!=null && title!="")
        	{
        		String newLocalUrl=title;
        		if (title.contains(sbolbase))
        		{
        			newLocalUrl=title.replace(sbolbase, "");
        		}
        		String newLocalId=newLocalUrl.replace("#", "");
        		
        		String oldLocalId=getAfter(href, "#");
        		link.attr("href", newLocalUrl);
        		Element divContainer=doc.getElementById(oldLocalId);
        		if (divContainer!=null) {
        			divContainer.attr("id",newLocalId);
        			 //addMissingComments(doc, divContainer, ontModel,newLocalId); 			
        		}
        	}
        }
        
        
        Model ontModel=getRdfModel();
        Property glyph=ontModel.createProperty(sbolbase + "defaultGlyph");
        Property glyphDir=ontModel.createProperty(sbolbase + "glyphDirectory");
         
        StmtIterator ri=ontModel.listStatements(null, glyph, (RDFNode) null);
        while (ri.hasNext())
        {
        	Statement stmt=ri.nextStatement();
        	Resource r= stmt.getSubject().asResource();
        	
        	//Get the name of the term
        	String uri=r.getURI();
        	
        	//Get the glyph name for the term
        	String value=stmt.getLiteral().asLiteral().getString();
        	
        	//Get the directory name, and find out the full glyph path
        	Statement stmtDir=r.getProperty(glyphDir);
        	String dir=stmtDir.getLiteral().asLiteral().getString();
        	dir=dir.replace("SBOL-visual/", "");        	
        	//value=String.format("https://github.com/SynBioDex/SBOL-visual/raw/master/%s/%s", dir, value);
        	value=String.format("http://synbiodex.github.io/SBOL-visual/%s/%s", dir, value);
        	
        	
        	//Find the dl tag to add the image in
        	//Find the a tag using the name
        	//Example a:  <a name="#AssociationGlyph"></a>
        	String aName="#" + uri.replace(sbolbase, "");        	
        	Element a=doc.selectFirst("a[name='" + aName + "']");
        	//e.g. doc.selectFirst("a[name='#DnaStabilityElementGlyph']")
        	Element div=a.parent();
        	Element dl=div.selectFirst("dl");
        	
        	//Add the image
        	String imageTag=String.format("<dt>default glyph</dt><dd><img src='%s'></dd>", value);
        	dl.append(imageTag); 	
        }
        
        
        cleanHeaders(doc);
        
        //final File f = new File("../sbol-vo.html");
        FileUtils.writeStringToFile(source, doc.outerHtml(), "UTF-8");
        System.out.println( "done!" );
    }
    
    private static String getAfter(String data, String separator)
    {
    	int index=data.indexOf(separator);
    	if (index>=0)
    	{
    		return data.substring(index+separator.length());
    	}
    	else
    	{
    		return data;
    	}
    }
    private static void cleanHeaders(Document doc)
    {
    	Elements heads=doc.select("div.head");
    	if (heads!=null)
    	{ 
    		Element head= heads.first();
    		Elements dls=head.getElementsByTag("dl");
    		int i=0;
    		ArrayList<Element> toRemove=new ArrayList<Element>();
    		
    	    for (Element el:dls)
    		{
    			if (i>=1)
    			{
    				toRemove.add(el);
    			}
    			i++;
    		}
    		for (Element el:toRemove)
    		{
    			el.remove();
    		}
    	}
    	
    }
    private  static void addMissingComments(Document doc, Element divContainer, Model ontModel, String sbolName)
    {
    	Elements comments=divContainer.getElementsByAttributeValueContaining("class", "comment");
		if (comments==null || comments.size()==0)
		{
			Elements descriptions=divContainer.getElementsByAttributeValueContaining("class", "description");
			if (descriptions!=null && descriptions.size()>0)
			{
				String commentString=getProperty(ontModel, sbolbase + "#" + sbolName, "http://www.w3.org/2000/01/rdf-schema#comment");
				if (commentString!=null)
				{
					Element description=descriptions.first();
					Element comment=createCommentElement(doc, divContainer, commentString);	
					comment.before(description);
				}
			}
		}  
    }
    private static String getProperty(Model ontModel, String resourceUri, String propertyUri)
    {
    	String value=null;
    	Resource resource= ontModel.getResource(resourceUri);
    	if (resource!=null)
    	{
    		Statement stmt=resource.getProperty(RDFS.comment);
    		if (stmt!=null)
    		{
    			value=stmt.getLiteral().getString();
    		}
    		else
    		{
    			System.out.println("No comment for " + resourceUri);
    		}
    	}
    	
    	return value;
    }
    private static Element createCommentElement (Document doc,Element parent, String commentString)
    {
    	//Element commentDiv=new Element("div");
    	Element commentDiv=doc.createElement("div");
    	commentDiv.appendTo(parent);
    	commentDiv.addClass("comment");
    	Element p=new Element("p");
    	p.appendText(commentString);
    	commentDiv.appendChild(p);
    	return commentDiv;
    }
    private static Model getRdfModel() throws IOException
    {
		Model model = ModelFactory.createDefaultModel();

		InputStream is = new FileInputStream("../sbol-vo.rdf");
		model.read(is, RDFS.getURI());

		return model;
    }
}
