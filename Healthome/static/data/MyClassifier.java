import java.util.ArrayList;

import extrapackage.FileHandler;
import extrapackage.NaiveBayes;
import extrapackage.Point;

public class MyClassifier {
	static public void main(String args[]){
		FileHandler trainingFileHandler = new FileHandler(args[0], args[1]);
		trainingFileHandler.processLines();
		ArrayList<Point> trainingPointsList = trainingFileHandler.getPointsList();
		
		NaiveBayes myNBClassifier = new NaiveBayes(trainingPointsList);
		trainingFileHandler.writeToFiles(myNBClassifier.toString());
	}
}
