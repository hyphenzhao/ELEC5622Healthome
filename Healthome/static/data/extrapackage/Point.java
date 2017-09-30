package extrapackage;

public class Point {
	private double data[] = new double[Default.ARRAY_LENGTH];
	private boolean result;
	private double distance;
	
	public Point(double data[], boolean result){
		this.data = data;
		this.result = result;		
		this.distance = Double.MAX_VALUE;
	}
	
	public void setDistance(double distance){
		this.distance = distance;
	}
	public void setResult(boolean result){
		this.result = result;
	}
	public double getDistance(){
		return this.distance;
	}
	public boolean getResult(){
		return this.result;
	}
	public double getDataAt(int index){
		return data[index];
	}
	
	public String toString(){
		String s = "";
		for(int i = 0; i < Default.ARRAY_LENGTH; i++){
			s += data[i] + ", ";
		}
		if(result){
			s += "yes";
		} else {
			s += "no";
		}
		return s;
	}
}
