import matplotlib.pyplot as plt
import random
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
    def visualize(self, ax=None):
        bottleneck_periods = self.find_bottlenecks()
        
        # Create a new figure if no ax object is provided
        if ax is None:
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

        # Display the plot if no ax object is provided
        if ax is None:
            plt.show()


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set window title to "APM"
        self.setWindowTitle("APM")
        
        # Add maximize and minimize buttons to window
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.input_label = QtWidgets.QLabel("Number of Resources:")
        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setText('5') # Set default value
        # self.input_field.setMaximumHeight(100) # Set minimum width of text box
        self.input_field.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred) # Set fixed horizontal size policy

        # Create label and text box for number of observations
        self.obs_label = QtWidgets.QLabel("Number of Observations:")
        self.obs_field = QtWidgets.QLineEdit()
        self.obs_field.setText('15') # Set default value
        # self.obs_field.setMinimumWidth(200) # Set minimum width of text box
        self.obs_field.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred) # Set fixed horizontal size policy

        self.button = QtWidgets.QPushButton("Perform APM")
        self.button.clicked.connect(self.perform_class)
        # self.button.setMinimumWidth(100) # Set minimum width of button
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred) # Set fixed horizontal size policy
        
        # Add QPlainTextEdit to display resource_states matrix
        self.matrix_label = QtWidgets.QLabel("Resource States Matrix:")
        self.matrix_display = QtWidgets.QPlainTextEdit()
        self.matrix_display.setReadOnly(True)
        # self.matrix_display.setMaximumWidth(200)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        
        # Create left layout
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.input_label)
        left_layout.addWidget(self.input_field)
        left_layout.addWidget(self.button)
        
        # Create right layout
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.matrix_label)
        right_layout.addWidget(self.matrix_display)
                 
        # Create upper layout
       # Create upper layout
        upper_layout = QtWidgets.QHBoxLayout()
        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.input_label)
        left_layout.addWidget(self.input_field)
        left_layout.addWidget(self.obs_label)
        left_layout.addWidget(self.obs_field)
        left_layout.addWidget(self.button)
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addWidget(self.matrix_label)
        right_layout.addWidget(self.matrix_display)
        upper_layout.addLayout(left_layout)
        upper_layout.addLayout(right_layout)
        
        # Create lower layout
        lower_layout = QtWidgets.QVBoxLayout()
        lower_layout.addWidget(self.canvas)
        
        # Create splitter to make segments resizable by mouse and set stretch factor
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        upper_widget = QtWidgets.QWidget()
        upper_widget.setLayout(upper_layout)
        lower_widget = QtWidgets.QWidget()
        lower_widget.setLayout(lower_layout)
        splitter.addWidget(upper_widget)
        splitter.addWidget(lower_widget)
        splitter.setStretchFactor(0, 1) # Set stretch factor of upper widget to 1
        splitter.setStretchFactor(1, 4) # Set stretch factor of lower widget to 4

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

               # Change font size of widgets in upper layout to 14
        font = QtGui.QFont()
        font.setPointSize(10)
        for widget in [self.input_label, self.input_field, self.obs_label, self.obs_field, self.button, self.matrix_label, self.matrix_display]:
            widget.setFont(font)

    def perform_class(self):
        num_resources_str = self.input_field.text()
        num_observations_str = self.obs_field.text()
        # Check if input field is empty
        if not num_resources_str:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter the number of resources')
            return
        
        num_resources = int(num_resources_str)
        num_observations = int(num_observations_str)
        # Generate random resource states
        resource_states = []
        for i in range(num_resources):
            sublist = [random.randint(0, 1) for j in range(num_observations)]
            resource_states.append(sublist)
              # Display resource_states matrix in matrix_display widget

        matrix_str = '\n'.join([' '.join(map(str, row)) for row in resource_states])
        self.matrix_display.setPlainText(matrix_str)
        
        # Create ResourceTracker instance and perform calculations
        tracker = ResourceTracker(resource_states)
        active_periods = tracker.active_periods()
        bottlenecks = tracker.find_bottlenecks()
        shifting_bottleneck = tracker.ShiftingBottleneck()
        
        # Visualize results in embedded matplotlib graph
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.clear()
        tracker.visualize(ax=ax)
        self.canvas.draw()



        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())