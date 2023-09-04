import logging
import os
import uvicorn
from srcs import logging_setup

if __name__ == '__main__':
    logging_setup.setup()
    logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')
    uvicorn.run("server:app", host='0.0.0.0', port=int(os.getenv('PORT')), log_config='logging.yaml')