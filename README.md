# Network Traffic and Queue Length Analysis in Mininet

This repository presents an implementation and analysis of network traffic generation and queue length measurement in a simulated Mininet environment. The study investigates the impact of bandwidth constraints and traffic intensity on network performance, specifically focusing on queue length dynamics.

## Key Features

* **Traffic Generation:** Python's Scapy module is used to generate network traffic with exponential inter-arrival times and fixed packet lengths, simulating realistic traffic patterns.
* **Bandwidth Limitation:** TCLink is employed to control link bandwidth, allowing for the investigation of network behavior under various bandwidth constraints.
* **Queue Length Measurement:** Queue length measurements are captured in the Mininet environment and compared with theoretical predictions from the M/G/1 queueing model, providing insights into queue dynamics.
* **Performance Metrics:** Latency and throughput measurements are obtained using ping and iperf, offering a comprehensive view of network performance under different traffic conditions.

## Implementation Details

* **Mininet:** The network topology and simulation environment are implemented in Mininet, a popular network emulation platform.
* **Python:** Python scripts are used for traffic generation, queue length measurement, and data analysis.
* **Scapy:** The Scapy module enables the creation and manipulation of network packets for realistic traffic generation.
* **TCLink:** TCLink is utilized to control link bandwidth, providing flexibility in simulating different network conditions.
* **M/G/1 Queueing Model:** Theoretical queue length predictions are derived from the M/G/1 queueing model, serving as a benchmark for comparison with empirical measurements.

## Findings

* **Bandwidth Impact:** The study demonstrates the significant influence of bandwidth limitations on network performance, particularly under high traffic loads.
* **Traffic Intensity:** Traffic intensity is shown to be a key factor in queue length dynamics, with higher traffic loads leading to increased queue lengths and potential congestion.
* **M/G/1 Model:** The M/G/1 queueing model provides valuable insights into queue behavior, although deviations from theoretical predictions may occur under certain conditions.

## Usage

1. **Clone the repository:** `git clone git@github.com:hxngillani/Teletraffic-Engineering-Project.git`
2. **Install Mininet:** Follow the Mininet installation instructions for your operating system.
3. **Run the Python scripts:** Execute the provided Python scripts to generate traffic, measure queue lengths, and analyze performance metrics.
4. **Explore the results:** Examine the collected data and compare empirical queue length measurements with theoretical predictions.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance this project.

## License

This project is licensed under the MIT License.

## Acknowledgments

This study was inspired by the need to understand the complex interplay between network traffic, bandwidth constraints, and queue dynamics. We acknowledge the valuable contributions of the Mininet, Scapy, and TCLink communities in enabling this research.
