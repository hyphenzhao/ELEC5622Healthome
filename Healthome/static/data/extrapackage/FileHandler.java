package extrapackage;
import java.util.ArrayList;
import java.io.*;

public class FileHandler {
	private String inputFileName, outputFileName;
	private int index = 0;
	private ArrayList<String> rawTextLine = new ArrayList<String>();
	private ArrayList<Point> points = new ArrayList<Point>();
	
	public FileHandler(String inputFileName, String outputFileName){
		this.inputFileName = inputFileName;
		this.outputFileName = outputFileName;
		try{
			File file = new File(this.inputFileName);
			if (file.isFile() && file.exists())
	        {
	            InputStreamReader inputStream = new InputStreamReader(
	                    new FileInputStream(file));
	            BufferedReader bufferedReader = new BufferedReader(inputStream);
	            String lineText = null;

	            while ((lineText = bufferedReader.readLine()) != null)
	            {
	                rawTextLine.add(lineText);
	            }
	            bufferedReader.close();
	            inputStream.close();
	        }
		} catch(Exception e){
			System.out.println("Input file error.");
			e.printStackTrace();
		}
	}
	
	public void processLines(){
		int i = 0;
		while(i < rawTextLine.size() && !rawTextLine.get(i).equals("")){
			String rawdata[] = rawTextLine.get(i).split(",");
			double para[] = new double[Default.ARRAY_LENGTH];
			for(int j = 0; j < Default.ARRAY_LENGTH; j++){
				para[j] = Double.parseDouble(rawdata[j]);
			}
			if(rawdata.length > Default.ARRAY_LENGTH && rawdata[Default.ARRAY_LENGTH].equals("yes")){
				points.add(new Point(para, true));
			} else {
				points.add(new Point(para, false));
			}
			i++;
		} 
	}
	
	public String getNextRawDataLine(){
		if(index < rawTextLine.size() && !rawTextLine.get(index).equals("")){
			return rawTextLine.get(index++);
		}
		return "";
	}
	
	public ArrayList<Point> getPointsList(){
		return this.points;
	}

	public void writeToFiles(String output){
		try{
			BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName));
    		writer.write(output);
    		writer.close();
		} catch(Exception e) {
			System.out.println("Output file error.");
			e.printStackTrace();
		}
	}
}
