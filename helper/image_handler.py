from io import BytesIO
import base64
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def encode_img2b64(fig: Figure) -> str:
    buffer=BytesIO()
    plt.savefig(buffer, format='png',bbox_inches="tight", dpi=70 ) #save fig into buffer
    buffer.seek(0)
    encoded_image=base64.b64encode(buffer.read())
    buffer.close()
    plt.close(fig)
    return encoded_image.decode('utf-8')