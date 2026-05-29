import os
import hopsworks

os.environ["TMPDIR"] = "C:/tmp"


project = hopsworks.login(
    project="A_Q_I_P",
    api_key_value="dIHUaXgn5ma9oLPx.pclDo5CA72LP7jWzF0nKQPjHiDo2CjR6SGxiIk6DmsDS55u6GFHQ1iVPx9a2qwLr"
)

print("CONNECTED SUCCESSFULLY")
fs = project.get_feature_store()