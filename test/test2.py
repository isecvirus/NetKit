import yaml

from util.util import *


# f0:f1:f2:f3:f4:f5 > 240:241:242:243:244:245
# f0:f1:f2:f3:f4:f5 > 11110000:11110001:11110010:11110011:11110100:11110101

print(isipv4("66.99.66.99"))

print(yaml.safe_load(open("../utilities.yml").read()))