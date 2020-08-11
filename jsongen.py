import apiworks
import json

f = apiworks.api()
f.refresh()
f.exportStar()
print(f.importStar())
