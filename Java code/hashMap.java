import java.util.*;

public class hashMap {
	public static void add(String s, int n, HashMap<String, Integer> map){
		map.put(s, n);
		System.out.println("Added");
		System.out.println(map);
	}
	public static void find(String s, HashMap<String, Integer> map){
		Integer x = map.get(s);
		System.out.println(s+" found. Key: " + x);
	}
	public static void main(String[] args){
		Scanner sc = new Scanner(System.in);
		HashMap<String, Integer> map = new HashMap<String, Integer>();
		map.put("a", 10);
		map.put("b", 20);
		map.put("c", 30);
		System.out.println("Size of map: "+ map.size());
		System.out.println(map);
		int choice;
		char ans='y';
		do{
			System.out.println("\nMain menu");
			System.out.println("1.ADD \n2.FIND ");
			System.out.println("Enter your choice: ");
			Scanner input = new Scanner(System.in);
			choice = input.nextInt();
			switch(choice){
			case 1:
				System.out.println("Enter element to add: ");
				String str = sc.nextLine();
				System.out.println("Enter key: ");
				int n = sc.nextInt();
				add(str, n, map);
				break;
			case 2:
				System.out.println("Enter element to find: ");
				String st = sc.nextLine();
				find(st, map);
				break;
			}
			System.out.println("Do you want to continue? (y/n): ");
			ans = input.next().charAt(0);
		}
		while(ans=='y');
	}
}
