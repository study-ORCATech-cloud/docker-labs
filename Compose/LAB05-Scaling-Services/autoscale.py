import time
import subprocess
import docker

client = docker.from_env()

def get_cpu_usage(container):
    stats = container.stats(stream=False)
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    if system_delta > 0:
        return (cpu_delta / system_delta) * 100
    return 0

def get_average_cpu(service_name):
    containers = client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"})
    if not containers:
        return 0
    total_cpu = sum(get_cpu_usage(container) for container in containers)
    return total_cpu / len(containers)

def scale_service(service_name, replicas):
    subprocess.run(["docker", "compose", "up", "-d", "--scale", f"{service_name}={replicas}"])
    print(f"Scaled {service_name} to {replicas} replicas")

def autoscale():
    min_replicas = 2
    max_replicas = 10
    scale_up_threshold = 70  # CPU percentage
    scale_down_threshold = 30  # CPU percentage
    service_name = "web"
    
    while True:
        try:
            avg_cpu = get_average_cpu(service_name)
            current_replicas = len(client.containers.list(filters={"label": f"com.docker.compose.service={service_name}"}))
            
            print(f"Service: {service_name}, Replicas: {current_replicas}, Avg CPU: {avg_cpu:.2f}%")
            
            if avg_cpu > scale_up_threshold and current_replicas < max_replicas:
                scale_service(service_name, current_replicas + 1)
            elif avg_cpu < scale_down_threshold and current_replicas > min_replicas:
                scale_service(service_name, current_replicas - 1)
                
            time.sleep(30)  # Check every 30 seconds
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Wait longer if there's an error

if __name__ == "__main__":
    autoscale() 