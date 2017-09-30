package extrapackage;
import java.util.ArrayList;
import java.lang.Math;

public class NaiveBayes {
	private ArrayList<Point> trainingPoints;
	
	private double yesAttributeMean[] = new double[Default.ARRAY_LENGTH];
	private double yesAttributeSD[] = new double[Default.ARRAY_LENGTH];
	private double yesAttributeData[];
	private int yesSize = 0;
	
	private double noAttributeMean[] = new double[Default.ARRAY_LENGTH];
	private double noAttributeSD[] = new double[Default.ARRAY_LENGTH];
	private double noAttributeData[];
	private int noSize = 0;
	
	public NaiveBayes(ArrayList<Point> points){
		this.trainingPoints = points;
		for(int i = 0; i < this.trainingPoints.size(); i++){
			if(this.trainingPoints.get(i).getResult())
				yesSize++;
			else
				noSize++;
		}
		noAttributeData = new double[noSize];
		yesAttributeData = new double[yesSize];
		for(int i = 0; i < Default.ARRAY_LENGTH; i++){
			int yes = 0, no = 0;
			for(int j = 0; j < this.trainingPoints.size(); j++){
				if(this.trainingPoints.get(j).getResult())
					yesAttributeData[yes++] = trainingPoints.get(j).getDataAt(i);
				else
					noAttributeData[no++] = trainingPoints.get(j).getDataAt(i);
			}
			noAttributeMean[i] = calculateMean(noAttributeData);
			noAttributeSD[i] = calculateSD(noAttributeData, noAttributeMean[i]);
			yesAttributeMean[i] = calculateMean(yesAttributeData);
			yesAttributeSD[i] = calculateSD(yesAttributeData, yesAttributeMean[i]);
		}
		
	}

	private double calculateMean(double input[]){
		double sum = 0.0;
		for(int i = 0; i < input.length; i++){
			sum += input[i];
		}
		
		if(input.length == 0) return 0.0;
		
		return sum/input.length;
	}
	private double calculateSD(double input[], double mean){
		double sum = 0.0;
		double n = (double) input.length;
		
		for(int i = 0; i < input.length; i++){
			sum += Math.pow(input[i] - mean, 2.0);
		}
		
		if(input.length == 0) return 0.0;
		
		return Math.sqrt(sum / n);
	}
	public String toString(){
		String str = "";

		str += yesSize + "," + noSize + "\n";
		for(int i = 0; i < Default.ARRAY_LENGTH; i++){
			str += yesAttributeMean[i] + "," + yesAttributeSD[i] + "," + noAttributeMean[i] + "," + noAttributeSD[i] + "\n";
		}

		return str;
	}
}
