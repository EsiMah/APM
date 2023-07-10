import matplotlib.pyplot as plt
import random

class ResourceTracker:
    def __init__(self, resource_states):
        self.resource_states = resource_states
        self.num_resources = len(resource_states)
        self.num_times = len(resource_states[0])

    def active_periods(self):
        active_periods = [[] for _ in range(self.num_resources)]
        current_start_time = [None] * self.num_resources

        for time in range(self.num_times):
            for resource in range(self.num_resources):
                if self.resource_states[resource][time] == 1:
                    if current_start_time[resource] is None:
                        current_start_time[resource] = time
                else:
                    if current_start_time[resource] is not None:
                        active_periods[resource].append((current_start_time[resource], time - 1))
                        current_start_time[resource] = None
                

        for resource in range(self.num_resources):
            if current_start_time[resource] is not None:
                active_periods[resource].append((current_start_time[resource], self.num_times - 1))

        return active_periods
       
    def find_bottlenecks(self):
        active_periods = self.active_periods()

        # Flatten the list, add resource name and sort by start time
        sorted_periods = sorted(((period, f'Resource {i}') for i, periods in enumerate(active_periods) for period in periods), key=lambda x: x[0][0])
        #print('sorted periods:',sorted_periods)
        bn_list = []
        last_bn_end = None
        last_bn_duration = None

        for period, resource in sorted_periods:
            start, end = period
            duration = end - start

            if last_bn_end is None:  # First run
                bn_list.append((period, resource))
                last_bn_end = end
                last_bn_duration = duration
            else:
                if end > last_bn_end or start > last_bn_end:  # End of entry is after last_bn_end
                    bn_list.append((period, resource))
                    last_bn_end = end
                    last_bn_duration = duration
                # elif start > last_bn_end:  # Start of entry is after last_bn_end
                #     bn_list.append((period, resource))
                #     last_bn_end = end
                #     last_bn_duration = duration

        return bn_list
    def ShiftingBottleneck (self):
        bottleneck_periods = self.find_bottlenecks()
        shifting_periods=[]
        for i in range(len(bottleneck_periods)):
            for j in range(i+1, len(bottleneck_periods)):
                _, end1 = bottleneck_periods[i][0]
                start2,_ = bottleneck_periods[j][0]
                if end1>start2:  # There is an overlap
                    overlap_start = start2
                    overlap_end = end1
                    shifting_periods.append(((max(overlap_start-1,0), overlap_end), bottleneck_periods[i][1], bottleneck_periods[j][1]))
        return shifting_periods
    def visualize(self):
        bottleneck_periods = self.find_bottlenecks()
        
        # Create a new figure
        fig, ax = plt.subplots()

        # Plot each resource's state over time
        for i, states in enumerate(self.resource_states):
            ax.plot([state + i*2 for state in states], drawstyle='steps', label=f'Resource {i}')

        # Highlight the bottleneck periods
        for period, resource in bottleneck_periods:
            start, end = period
            resource_num = int(resource.split(' ')[1])
            ax.fill_between(range(max(0,start-1), end+1), 2*resource_num+.8, 2*resource_num+1.2, color='red', alpha=0.3)

        # Set y-axis ticks and labels
        ax.set_yticks([i*2+0.5 for i in range(len(self.resource_states))])
        ax.set_yticklabels([f'Resource {i}' for i in range(len(self.resource_states))])

        # Set x-axis ticks and labels
        ax.set_xticks(range(len(self.resource_states[0])+1))
        ax.set_xticklabels(range(0, len(self.resource_states[0])+1))

        # Add labels and a legend
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Resource')
        ax.legend()

        # Display the plot
        plt.show()

# resource_states = [[1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0], 
#                    [0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0], 
#                    [1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1]]
resource_states = []
for i in range(5):
    sublist = [random.randint(0, 1) for j in range(15)]
    resource_states.append(sublist)
print (resource_states)

tracker = ResourceTracker(resource_states)
print (tracker.active_periods())
print(tracker.find_bottlenecks())
print(tracker.ShiftingBottleneck())
tracker.visualize()
# for resource, periods in enumerate(active_periods):
#     print(f"Resource {resource} has active periods: {periods}")