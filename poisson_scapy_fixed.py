import random
import time
import logging
import subprocess
from scapy.all import send
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

def get_tc_stats(iface):
    """Fetch transmission queue stats using `tc`."""
    try:
        result = subprocess.run(
            ['tc', '-s', 'qdisc', 'show', 'dev', iface],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.decode('utf-8')  # Decoding the output
    except Exception as e:
        print(f"Error fetching tc stats: {e}")
        return None

def get_backlog_size(tc_stats):
    """Extract backlog size from tc stats."""
    for line in tc_stats.split('\n'):
        if 'backlog' in line:
            parts = line.split()
            for i, part in enumerate(parts):
                if part == 'backlog':
                    size_part = parts[i + 1]
                    if 'Kb' in size_part:
                        return int(size_part.replace('Kb', '')) * 1000  # Convert Kb to bytes
                    elif 'b' in size_part:
                        return int(size_part.replace('b', ''))  # Bytes as is
    return 0

def calculate_service_time(packet_size, link_bw):
    """Calculate the service time for a packet based on packet size and link bandwidth."""
    bandwidth_bps = link_bw * 10**6  # Convert Mbps to bps
    return packet_size * 8 / bandwidth_bps  # Service time in seconds

def calculate_theoretical_queue_length(arrival_rate, service_rate):
    """Calculates the theoretical M/G/1 queue length with fixed packet length."""
    rho = arrival_rate / service_rate  # Traffic intensity (utilization)
    
    if rho >= 1:
        return float('inf')  # System is unstable

    # M/G/1 queue length formula (variance = 0 for fixed packet length)
    queue_length = (rho**2) / (2 * (1 - rho))
    
    return queue_length

def generate_packets_fixed_length(src_ip, dst_ip, iface, link_bw, lambda_arrival, packet_length, max_packets=50, backlog_threshold=50000):
    """Generate traffic with exponential inter-arrival times and fixed packet length."""
    logging.getLogger("scapy").setLevel(logging.CRITICAL)
    generated_packets = 0
    generated_bytes = 0
    total_waiting_time = 0  # To calculate cumulative waiting time
    start_time = time.time()  # Record the start time

    service_time = calculate_service_time(packet_length, link_bw)  # Calculate the service time for each packet
    previous_packet_end_time = start_time  # Track when the previous packet finished

    # Calculate service rate and initial theoretical queue length
    service_rate = (link_bw * 10**6) / (packet_length * 8)  # Service rate in packets/sec
    theoretical_queue_length_initial = calculate_theoretical_queue_length(lambda_arrival, service_rate)

    # Debugging output
    print(f"Service Rate: {service_rate:.2f} packets/sec")
    print(f"Theoretical Queue Length (Initial): {theoretical_queue_length_initial:.4f} packets")

    try:
        while generated_packets < max_packets:
            inter_arrival_time = random.expovariate(lambda_arrival)
            time.sleep(inter_arrival_time)  # Simulating packet arrival

            # Create a fixed-size payload
            packet_data = bytearray(random.getrandbits(8) for _ in range(packet_length))

            # Create the packet (Ethernet + IP + Raw payload)
            packet = Ether() / IP(src=src_ip, dst=dst_ip) / Raw(load=packet_data)

            # Track when the packet is sent (service starts)
            send_start_time = time.time()

            # Calculate waiting time
            waiting_time = max(0, send_start_time - previous_packet_end_time)
            total_waiting_time += waiting_time  # Add waiting time for this packet

            # Send the packet
            send(packet, iface=iface, verbose=False)

            # Simulate transmission service time
            send_end_time = send_start_time + service_time
            total_time_in_system = waiting_time + service_time

            # Update packet counters and stats
            generated_packets += 1
            generated_bytes += packet_length
            elapsed_time = time.time() - start_time
            packet_arrival_rate = generated_packets / elapsed_time

            # Fetch transmission queue stats and check backlog size
            tc_stats = get_tc_stats(iface)
            backlog_size = get_backlog_size(tc_stats)

            # Calculate average waiting time
            avg_waiting_time = total_waiting_time / generated_packets if generated_packets > 0 else 0

            # Calculate theoretical queue lengths
            theoretical_queue_length_current = calculate_theoretical_queue_length(packet_arrival_rate, service_rate)
            actual_queue_length = backlog_size / packet_length  # Simplified actual queue length in packets

            # Log packet statistics
            print(f"\n### Packet {generated_packets} ###")
            print(f"Packet size: {packet_length} bytes")
            print(f"Service time: {service_time:.6f} seconds")
            print(f"Waiting time before transmission (in system): {waiting_time:.6f} seconds")
            print(f"Total time spent in the system: {total_time_in_system:.6f} seconds")
            print(f"Elapsed time since start: {elapsed_time:.2f} seconds")
            print(f"Current packet arrival rate: {packet_arrival_rate:.2f} packets per second")
            print(f"Average waiting time (across all packets): {avg_waiting_time:.6f} seconds")
            print(f"Current backlog size: {backlog_size} bytes")
            print(f"Theoretical queue length (initial parameters): {theoretical_queue_length_initial:.4f} packets")
            print(f"Theoretical queue length (current observed rate): {theoretical_queue_length_current:.4f} packets")
            print(f"Actual queue length: {actual_queue_length:.4f} packets")

            # Stop if backlog exceeds the threshold
            if backlog_size > backlog_threshold:
                print(f"\nBacklog size exceeded threshold of {backlog_threshold} bytes. Stopping packet generation.")
                break

            # Update the previous packet end time
            previous_packet_end_time = send_end_time

    except (OSError, KeyboardInterrupt) as e:
        print(f"\nError occurred: {e}")
        print("\nPacket generation interrupted. Summary:")
    finally:
        elapsed_time = time.time() - start_time
        if generated_packets > 0:
            avg_waiting_time = total_waiting_time / generated_packets
            final_packet_arrival_rate = generated_packets / elapsed_time
            
            print(f"\n### Final Summary ###")
            print(f"Total packets sent: {generated_packets}")
            print(f"Average packet length: {generated_bytes / generated_packets:.2f} bytes")
            print(f"Final packet arrival rate: {final_packet_arrival_rate:.2f} packets per second")
            print(f"Average waiting time (across all packets): {avg_waiting_time:.6f} seconds")

        # Fetch and print final `tc` stats
        final_tc_stats = get_tc_stats(iface)
        print(f"\nFinal Transmission Queue Stats:\n{final_tc_stats}")
        print("Exiting gracefully.")

