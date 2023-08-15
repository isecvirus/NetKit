package org.virus.netkit;

/**
 *
 * @author virus
 */
public class NetKit {

    String[] _all_ = {"b2i", "b2m", "c2h", "c2i", "c2n", "h2c", "i2b", "i2c", "i2i", "i2n", "i2p", "i2t", "isipv4", "m2b", "m2n",
        "n2c", "n2i", "n2m", "p2i", "r2c", "r2r", "t2i", "v2a", "p2d"};

    String PRIVATE = "private";
    String PUBLIC = "public";
    String LOOPBACK = "loopback";
    String LINK_LOCAL = "link-local";
    String MULTICAST = "multicast";
    String RESERVED = "reserved";
    String RESERVED_FOR_IANA = "Reserved for IANA";
    String IETF_PROTOCOL_ASSIGNMENT = "IETF Protocol Assignment";
    String CARRIER_GRADE_NAT = "Carrier-grade NAT";
    String TEST_NET_1 = "TEST-NET-1";

    static int MIN_PORT = 0;
    static int MAX_PORT = (int) Math.pow(2, 16) - 1;

    public static int isMAX_PORT(int port) {
        return port <= MAX_PORT ? port : MAX_PORT;
    }

    public static int binary_to_number(String binary) {
        int decimal = 0;
        for (String digit : binary.split("")) {
            decimal = decimal * 2 + Integer.parseInt(digit);
        }
        return decimal;
    }

    public static String number_to_binary(int decimal, boolean fill) {
        String binary_octet = "";

        while (decimal > 0) {
            int remainder = decimal % 2;
            binary_octet = String.valueOf(remainder) + binary_octet;
            decimal = decimal / 2;
        }
        return fill ? String.format("%8s", binary_octet).replace(" ", "0") : binary_octet;
    }

    public static boolean isipv4(String ipv4, String sep) {
        try {
            boolean dots = String.valueOf(new MyString(ipv4).count('.')).equals("3");
            
            if (!dots) return false;
            
            String[] octets = ipv4.split(sep);
            for (int i=0;i<octets.length;i++) {
                int oct = Integer.parseInt(octets[i]);

                if (!(oct >= 0 || oct <= 255)) return false;
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public static void main(String[] args) {
        System.out.println(isipv4("257.0.0.0", "."));
    }
}

class MyString {
    private final String str;

    public MyString(String str) {
        this.str = str;
    }

    public int count(char c) {
        int num = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == c) {
                num += 1;
            }
        }
        return num;
    }
}
