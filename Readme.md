# Setting up the Environment


Getting venv with Python3.12 working:
# Adjust for your python version
sudo apt-get install python3.12-venv
Found here: https://askubuntu.com/questions/1469080/ubuntu-23-04-python3-no-module-named-ensurepip

*Running docker compose:*
Instead of using `docker-compose`, use `docker compose` as i had the same issue when i upgraded my ubuntu to 24.10. Also you will need to give sudo permissions as those were needed for it to work and then reboot and try.
https://github.com/rashadphz/farfalle/issues/32#issuecomment-2142280468
