
import java.io.*;
import java.util.*;
import java.net.*;

public class Master {
    public static void main(String args[]) throws Exception {
        String send = "", r = "";
        Socket MyClient = new Socket("192.168.0.106", 25);
        System.out.println("Connected as Master");
        DataInputStream din = new DataInputStream(MyClient.getInputStream());
        DataOutputStream dout = new DataOutputStream(MyClient.getOutputStream());
        Scanner sc = new Scanner(System.in);
        do {
            System.out.print("Message('close' to stop): ");
            send = sc.nextLine();
            dout.writeUTF(send);
            dout.flush();
        } while (!send.equals("stop"));
        dout.close();
        din.close();
        MyClient.close();
    }
}
