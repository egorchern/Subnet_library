def bitwise_and(left_operand, right_operand):
    ans = "";
    for i in range(0, len(left_operand)):
        left_char = left_operand[i];
        right_char = right_operand[i];
        if left_char == "1" and right_char == "1":
            ans += "1";
        else:
            ans += "0";
    return ans;
    
def bitwise_nand(left_operand, right_operand):
    and_result = bitwise_and(left_operand, right_operand);
    ans = "";
    for char in and_result:
        if(char == "1"):
            ans += "0";
        else:
            ans += "1";
    return ans;

def bitwise_or(left_operand, right_operand):
    ans = "";
    for i in range(0, len(left_operand)):
        left_char = left_operand[i];
        right_char = right_operand[i];
        if left_char == "1" or right_char == "1":
            ans += "1";
        else:
            ans += "0";
    return ans;

def to_byte(binary):
    length = len(binary);
    ans = binary;
    for i in range(length, 8):
        ans = "0" + ans;
    return ans;

def to_binary(number):
    number = int(number);
    ans = [];
    powers_of_two = [1];
    stop_loop = False;
    while(stop_loop == False):
        next_number = powers_of_two[0] * 2;
        if next_number > number:
            stop_loop = True;
        else:
            powers_of_two.insert(0, next_number);
    running_result = number;
    for i in range(0, len(powers_of_two)):
        power = powers_of_two[i];
        temp = running_result - power;
        if(temp < 0):
            ans.append("0");
        else:
            running_result -= power;
            ans.append("1");
    ans_as_string = ''.join(ans);
    return ans_as_string;

def to_binary_octets(address):
    octets = str.split(address, ".");
    octets_as_binary = [];
    for i in range(0, len(octets)):
        octets_as_binary.append(to_byte(to_binary(octets[i])));
    return octets_as_binary;

def to_int(binary):
    powers_of_two = [1];
    for i in range(len(binary), 1, -1):
        next_power = powers_of_two[0] * 2;
        powers_of_two.insert(0, next_power);
    running_result = 0;
    for i in range(0, len(binary)):
        char = binary[i];
        if(char == "1"):
            running_result += powers_of_two[i];
    return str(running_result);

def get_network_id(ip_binary_octets, mask_binary_octets):
    binary_net_id = [];
    for i in range(0, len(ip_binary_octets)):
        ip_binary_octet = ip_binary_octets[i];
        mask_binary_octet = mask_binary_octets[i];
        and_result = bitwise_and(ip_binary_octet, mask_binary_octet);
        binary_net_id.append(and_result);
    net_id = [];
    for binary in binary_net_id:
        num = to_int(binary);
        net_id.append(num);
    return '.'.join(net_id);

def get_mask_length(mask_binary_octets):
    br_point = 0;
    for i in range(0, len(mask_binary_octets)):
        mask_octet = mask_binary_octets[i];
        for j in range(0, len(mask_octet)):
            char = mask_octet[j];
            if(char == "1"):
                br_point += 1;
    return br_point;

def get_host_id(ip_binary_octets, mask_binary_octets):
    binary_host_id = [];
    mask_length = get_mask_length(mask_binary_octets);
    octet = int(mask_length / 8);
    bit = mask_length % 8;
    for i in range(0, octet):
        binary_host_id.append("00000000");
    if(bit != 0):
        ip_portion = ip_binary_octets[octet][bit:8];
        mask_portion = mask_binary_octets[octet][bit:8];
        or_result = bitwise_or(ip_portion, mask_portion);
        or_result = to_byte(or_result);
        binary_host_id.append(or_result);
        octet += 1;
    while(len(binary_host_id) != 4):
        ip_portion = ip_binary_octets[octet]
        mask_portion = mask_binary_octets[octet]
        or_result = bitwise_or(ip_portion, mask_portion);
        #or_result = to_byte(or_result);
        binary_host_id.append(or_result);

    host_id = [];
    for binary in binary_host_id:
        num = to_int(binary);
        host_id.append(num);
    return '.'.join(host_id);

def get_broadcast_id(ip_binary_octets, mask_binary_octets):
    broadcast_id = ["", "", "", ""];
    br_point = get_mask_length(mask_binary_octets);
    counter = 0;
    while(counter < br_point):
        octet_num = int(counter / 8);
        bit_num = counter % 8;
        ip_octet = ip_binary_octets[octet_num];
        char = ip_octet[bit_num];
        broadcast_id[octet_num] += char;
        counter += 1;
    for i in range(0, len(broadcast_id)):
        octet = broadcast_id[i];
        while(len(octet) < 8):
            octet += "1";
        broadcast_id[i] = octet;
    int_broadcast_id = [];
    for i in range(0, len(broadcast_id)):
        num = to_int(broadcast_id[i]);
        int_broadcast_id.append(num);
    return ".".join(int_broadcast_id);


def get_network_and_broadcast_addresses(ip, subnet_mask):
    ip_binary_octets = to_binary_octets(ip);
    mask_binary_octets = to_binary_octets(subnet_mask);
    network_address = get_network_id(ip_binary_octets, mask_binary_octets);
    broadcast_id = get_broadcast_id(ip_binary_octets, mask_binary_octets);
    host_id = get_host_id(ip_binary_octets, mask_binary_octets);
    print("f");

def main():
    get_network_and_broadcast_addresses("90.195.132.36", "255.255.192.0");

if __name__ == "__main__":
    main();