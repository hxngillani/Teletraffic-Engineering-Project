# -*- coding: utf-8 -*-
import math
import argparse

def calculate_theoretical_queue_length(arrival_rate, service_rate):
    """Calculates the theoretical M/G/1 queue length with fixed packet length."""
    rho = arrival_rate / service_rate  # Traffic intensity (utilization)
    
    print("\n### Intermediate Calculations ###")
    print("Service Rate (packets/sec): {:.4f}".format(service_rate))
    print("Traffic Intensity (ρ): {:.4f}".format(rho))
    
    if rho >= 1:
        print("System is unstable (ρ >= 1). Queue length would be infinite.")
        return float('inf')  # System would be unstable

    # M/G/1 queue length formula (variance = 0 for fixed packet length)
    queue_length = (rho**2) / (2 * (1 - rho))
    
    print("Queue Length Formula: L_q = (ρ^2) / (2 * (1 - ρ))")
    print("Numerator (ρ^2): {:.4f}".format(rho**2))
    print("Denominator (2 * (1 - ρ)): {:.4f}".format(2 * (1 - rho)))
    
    return queue_length

def run_theoretical_queue_calculation(link_bw, arrival_rate, packet_size):
    print("Calculating theoretical queue length for link bandwidth: {} Mbps, "
          "arrival rate: {} packets/sec, packet size: {} bytes".format(link_bw, arrival_rate, packet_size))

    # Calculate service rate based on link bandwidth
    bandwidth_bps = link_bw * 10**6  # Convert Mbps to bps
    service_rate = bandwidth_bps / (packet_size * 8)  # Packets per second

    # Theoretical queue length (variance = 0 for fixed packet length)
    theoretical_queue_length = calculate_theoretical_queue_length(arrival_rate, service_rate)

    # Print theoretical queue length
    print("\n### Theoretical Queue Length (M/G/1) ###")
    print("Theoretical queue length: {:.4f} packets".format(theoretical_queue_length))

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Calculate theoretical M/G/1 queue length.")

    # Define command-line arguments
    parser.add_argument('--link_bw', type=float, required=True, help="Link bandwidth in Mbps")
    parser.add_argument('--arrival_rate', type=float, required=True, help="Packet arrival rate (packets/sec)")
    parser.add_argument('--packet_size', type=int, required=True, help="Packet size in bytes")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the theoretical queue calculation with parsed arguments
    run_theoretical_queue_calculation(args.link_bw, args.arrival_rate, args.packet_size)

if __name__ == '__main__':
    main()

