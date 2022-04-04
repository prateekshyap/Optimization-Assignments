import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.File;
import java.io.IOException;
import java.io.FileNotFoundException;

import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;
//import java.util.Comparable;

class Variable
{
	private boolean sign;
	private double coeff;
	private String varName;
	Variable()
	{
		this.sign = true;
		this.coeff = 0;
		this.varName = "";
	}
	Variable(String sign, double coeff, String varName)
	{
		this.sign = sign.equals("+") ? true : false;
		this.coeff = coeff;
		this.varName = varName;
	}
	public void setSign(String sign) { this.sign = sign.equals("+") ? true : false; }
	public void setCoeff(double coeff) { this.coeff = coeff; }
	public void setvarName(String varName) { this.varName = varName; }

	public String getSign() { return this.sign ? "+" : "-"; }
	public double getCoeff() { return this.coeff; }
	public String getVarName() { return this.varName; }

	public void printVar()
	{
		System.out.print((sign ? "+ " : "- ")+coeff+" "+varName+" ");
	}
}

class Simplex
{
	public static void main(String[] args) throws IOException
	{
		BufferedReader cmdReader, fileReader;
		String fileName, line, mode = "", sign, varName, target = "";
		String[] tokens;
		ArrayList<Variable> z = new ArrayList<Variable>();
		ArrayList<Variable> Ai = new ArrayList<Variable>();
		ArrayList<ArrayList<Variable>> A = new ArrayList<ArrayList<Variable>>();
		ArrayList<String> comp = new ArrayList<String>();
		ArrayList<Double> b = new ArrayList<Double>();
		ArrayList<Double> limits = new ArrayList<Double>();
		HashMap<String,ArrayList<Double>> bounds = new HashMap<String,ArrayList<Double>>();
		int index, j;
		double coeff;

		cmdReader = new BufferedReader(new InputStreamReader(System.in));
		fileName = cmdReader.readLine();
		fileReader = new BufferedReader(new FileReader(new File(fileName)));
		
		while ((line = fileReader.readLine()) != null)
		{
			tokens = line.trim().split(" +");
			if (tokens[0].equalsIgnoreCase("Maximize") || tokens[0].equalsIgnoreCase("Minimize") || tokens[0].equalsIgnoreCase("Subject") || tokens[0].equalsIgnoreCase("Bounds") || tokens[0].equalsIgnoreCase("General"))
			{
				target = tokens[0].equalsIgnoreCase("Maximize") || tokens[0].equalsIgnoreCase("Minimize") ? tokens[0] : target;
				mode = tokens[0];
				continue;
			}
			index = 0;
			if (mode.equalsIgnoreCase("Maximize") || mode.equalsIgnoreCase("Minimize"))
			{
				index = 1;
				sign = "+";
				coeff = 1;
				while (index < tokens.length)
				{
					if (tokens[index].equals("-")) sign = "-";
					else if (isNumber(tokens[index])) coeff = Double.parseDouble(tokens[index]);
					else if (!tokens[index].equals("+"))
					{
						varName = tokens[index];
						Variable newVar = new Variable(sign, coeff, varName);
						z.add(newVar);
						sign = "+";
						coeff = 1;
					}
					++index;
				}
			}
			else if (mode.equalsIgnoreCase("Subject"))
			{
				Ai = new ArrayList<Variable>();
				index = 1;
				sign = "+";
				coeff = 1;
				while (index < tokens.length)
				{
					if (tokens[index].equals("-")) sign = "-";
					else if (isNumber(tokens[index])) coeff = Double.parseDouble(tokens[index]);
					else if (tokens[index].equals(">") || tokens[index].equals("<") || tokens[index].equals(">=") || tokens[index].equals("<=") || tokens[index].equals("="))
					{
						comp.add(tokens[index]);
						break;
					}	
					else if (!tokens[index].equals("+"))
					{
						varName = tokens[index];
						Variable newVar = new Variable(sign, coeff, varName);
						Ai.add(newVar);
						sign = "+";
						coeff = 1;
					}
					++index;
				}
				A.add(Ai);
				b.add(Double.parseDouble(tokens[index+1]));
			}
			else if (mode.equalsIgnoreCase("Bounds"))
			{
				limits = new ArrayList<Double>();
				limits.add(Double.parseDouble(tokens[0]));
				limits.add(Double.parseDouble(tokens[4]));
				bounds.put(tokens[2],limits);
			}
			else if (mode.equalsIgnoreCase("General"))
			{}
		}

		System.out.println(target);
		for (int i = 0; i < z.size(); ++i)
			((Variable)z.get(i)).printVar();
		System.out.println();
		System.out.println("Subject To");
		for (int i = 0; i < A.size(); ++i)
		{
			Ai = (ArrayList)A.get(i);
			for (j = 0; j < Ai.size(); ++j)
				((Variable)Ai.get(j)).printVar();
			System.out.print(" "+comp.get(i));
			System.out.print(" "+b.get(i));
			System.out.println();
		}
		System.out.println("Bounds");
		Iterator it = bounds.entrySet().iterator();
		while (it.hasNext())
		{
			Map.Entry element = (Map.Entry)it.next();
			limits = (ArrayList)element.getValue();
			System.out.println(limits.get(0)+" <= "+element.getKey()+" <= "+limits.get(1));
		}

		fileReader.close();
	}

	public static boolean isNumber(String str)
	{
		boolean dotFound = false;
		for (char ch : str.toCharArray())
		{
			if (!(ch >= '0' && ch <= '9'))
			{
				if (ch != '.') return false;
				else if (dotFound) return false;
				if (ch == '.') dotFound = true;
			}
		}
		return true;
	}
}