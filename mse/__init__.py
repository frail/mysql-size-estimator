import warnings
import re

warnings.filterwarnings('always', category=DeprecationWarning,module='^{0}\.'.format(re.escape(__name__)))