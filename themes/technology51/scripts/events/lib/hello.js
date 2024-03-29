"use strict";

module.exports = (hexo) => {
  const isZh = hexo.theme.i18n.languages[0].search(/zh-CN/i) !== -1;
  if (isZh) {
    hexo.log.info(`
-------------------------------------------
    ___  ___                         
    |  \\/  |                         
    | .  . | __ _ _ __ ___ _   _ ___ 
    | |\\/| |/ _' | '__/ __| | | / __|
    | |  | | (_| | | | (__| |_| \\__ \\
    \\_|  |_/\\__,_|_|  \\___|\\__,_|___/
    
    GitHub: https://github.com/SuperBaBa
-------------------------------------------                                   
`);
  } else {
    hexo.log.info(`
-------------------------------------------
    ___  ___                         
    |  \/  |                         
    | .  . | __ _ _ __ ___ _   _ ___ 
    | |\/| |/ _' | '__/ __| | | / __|
    | |  | | (_| | | | (__| |_| \__ \
    \_|  |_/\__,_|_|  \___|\__,_|___/
    
    GitHub: https://github.com/SuperBaBa
-------------------------------------------  
`);
  }
};
