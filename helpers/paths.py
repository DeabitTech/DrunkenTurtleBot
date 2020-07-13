from pathlib import Path

projectPath = Path("./").absolute()

config = Path(projectPath/"config")
idConfig = Path(config/"idConfig.json")
sessionConfig = Path(config/"sessionConfig.json")
marketsConfig = Path(config/"marketsConfig.json")
clientConfig = Path(config/"clientConfig.json")

log = Path(projectPath/"log")
session_logs = Path(log/"session_logs")
rawLog = Path(log/"rawLog.txt")
eventLog = Path(log/"eventLog.txt")
errorLog = Path(log/"errorLog.txt")
newOrdersLog = Path(log/"newOrdersLog.csv")

