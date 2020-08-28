import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def get_image():
    # Creates a bytes buffer for the image to save.
    buffer = BytesIO()
    # Create the plot with the use of BytesIO object as its 'file'
    plt.savefig(buffer, format="png")
    # Set the cursor to the begining of the stream.
    buffer.seek(0)
    # retrive the entire content of the file.
    image_png = buffer.getvalue()

    # encode the image with the help of base64
    graph = base64.b64encode(image_png)
    # decode the image in watchable format utf-8
    graph = graph.decode("utf-8")

    # free the memory of the buffer.
    buffer.close()

    # return the graph
    return graph

def get_simple_plot(chart_type, *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,4))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    if chart_type == 'bar':
        title="Date Wise Total Price (Bar)"
        plt.title(title)
        plt.bar(x,y)
    elif chart_type == "line":
        title="Date Wise Purchase Graph (Line)"
        plt.title(title)
        plt.plot(x,y)
    elif chart_type == "Transaction count plot (Count)":
        title="title"
        plt.title(title)
        sns.countplot('name',data=data)
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph = get_image()
    return graph