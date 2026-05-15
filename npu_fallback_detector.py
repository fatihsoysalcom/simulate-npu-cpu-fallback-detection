import time
import random

# --- Configuration for simulation (adjust these values to observe different outcomes) ---
EXPECTED_NPU_INFERENCE_TIME_MS = 10  # Expected time for NPU execution in milliseconds
MAX_ACCEPTABLE_INFERENCE_TIME_MS = 70 # Threshold for acceptable performance before flagging as fallback
SIMULATED_CPU_FALLBACK_FACTOR = 10   # How much slower CPU fallback is relative to NPU simulation

# --- Simulation of an AI inference task ---
def simulate_inference(is_npu_fallback=False):
    """
    Simulates an AI inference task.
    If is_npu_fallback is True, it simulates a slower CPU execution.
    """
    start_time = time.perf_counter()

    # Simulate some computation that represents AI inference
    base_operations = 1_000_000 # Base number of operations for "NPU" speed

    if is_npu_fallback:
        # Simulate a slower CPU execution (e.g., less optimized, more operations)
        # This represents the performance hit when NPU delegates fail.
        operations = base_operations * SIMULATED_CPU_FALLBACK_FACTOR
        # Add a small, variable delay to make it less predictable, like real-world
        time.sleep(random.uniform(0.005, 0.015) * SIMULATED_CPU_FALLBACK_FACTOR)
    else:
        # Simulate fast NPU execution
        operations = base_operations
        time.sleep(random.uniform(0.001, 0.003)) # Small NPU-like latency

    # Perform dummy computation
    result = 0
    for _ in range(operations // 1000): # Reduce actual loop iterations for faster execution of example
        result += random.random() * random.random()
    _ = result # Prevent unused variable warning

    end_time = time.perf_counter()
    return (end_time - start_time) * 1000 # Return time in milliseconds

# --- Main detection logic for CI environment ---
def run_performance_test(test_name, force_fallback=False):
    print(f"--- Running Test: {test_name} ---")
    print(f"  Expected NPU time: {EXPECTED_NPU_INFERENCE_TIME_MS:.2f} ms")
    print(f"  Max acceptable time: {MAX_ACCEPTABLE_INFERENCE_TIME_MS:.2f} ms")

    # Simulate running the AI model and measuring its performance.
    # In a real CI setup, this would involve executing the actual model
    # on target hardware (or an emulator) and capturing its execution time
    # using device-specific profiling tools or SDKs.
    inference_time = simulate_inference(is_npu_fallback=force_fallback)

    print(f"  Measured inference time: {inference_time:.2f} ms")

    # --- Core detection logic, mimicking a CI check ---
    if inference_time > MAX_ACCEPTABLE_INFERENCE_TIME_MS:
        # This condition signifies a critical performance regression,
        # likely due to an NPU fallback to CPU. A CI system would fail here.
        print("  🚨 CRITICAL: Potential NPU fallback detected! Performance is significantly degraded.")
        print("  This indicates the model might be running on CPU instead of NPU.")
        return False # Test failed
    elif inference_time > EXPECTED_NPU_INFERENCE_TIME_MS * 1.8: # A buffer for slight degradation
        # This condition indicates performance is worse than ideal NPU,
        # but not catastrophic. A CI system might issue a warning.
        print("  ⚠️ WARNING: Inference time is higher than expected for NPU. Investigate potential issues.")
        return True # Test passed, but with warning
    else:
        # Performance is within the expected range for NPU execution.
        print("  ✅ SUCCESS: Inference performance is within expected NPU range.")
        return True # Test passed

if __name__ == "__main__":
    print("Simulating NPU Fallback Detection in CI Environment\n")

    # Scenario 1: Model runs as expected on NPU
    print("Scenario 1: Model running optimally on NPU (simulated)")
    run_performance_test("Optimal NPU Performance Test", force_fallback=False)
    print("-" * 50 + "\n")

    # Scenario 2: Model silently falls back to CPU (simulated)
    # This scenario should trigger the CRITICAL warning.
    print("Scenario 2: Model silently falling back to CPU (simulated)")
    run_performance_test("NPU Fallback Detection Test", force_fallback=True)
    print("-" * 50 + "\n")

    # Scenario 3: Slightly degraded performance, but not a full fallback (simulated)
    # This scenario should trigger the WARNING.
    print("Scenario 3: Slightly degraded NPU performance (simulated)")
    # Temporarily adjust the fallback factor to simulate a less severe degradation
    original_cpu_fallback_factor = SIMULATED_CPU_FALLBACK_FACTOR
    SIMULATED_CPU_FALLBACK_FACTOR = 3 # Simulate a degradation that's not a full critical fallback
    run_performance_test("Degraded NPU Performance Test", force_fallback=True)
    SIMULATED_CPU_FALLBACK_FACTOR = original_cpu_fallback_factor # Reset for consistency
    print("-" * 50 + "\n")
