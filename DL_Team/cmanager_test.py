from PI_ClientManager import *

cli_manager = PI_ClientManager()
names = ["Josie", "Tammy", "Angela", "Pamela", "Josie", "Rita"]

for i in range(len(names)):
    cli_manager.add(names[i], i);
    cli_manager.p_all()
cli_manager.remove(0)
cli_manager.p_all()

for i in range(1,5):
    if ((i%2)==1):
        cli_manager.remove(i)
        cli_manager.p_all()
        cli_manager.add(names[1],i)
        cli_manager.p_all()
    else:
        cli_manager.remove(i)
        cli_manager.p_all()
        cli_manager.add(names[3],i)
        cli_manager.p_all()

for name in names:
    print(cli_manager.search(name))

cli_manager.remove(10)
cli_manager.p_all()
