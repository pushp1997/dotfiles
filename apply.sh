#! /bin/bash
printf "Installing yay"
sudo pacman -S --needed base-devel
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si
cd ../
rm -rf yay
yay -Syyu

printf "Installing dependencies\n"
yay -S xorg xorg-xinit qtile feh scrot udiskie ntfs-3g ttf-font-awesome ttc-iosevka picom htop harfbuzz ttf-hack-nerd ttf-joypixels brightnessctl network-manager-applet ttf-ubuntu-font-family dunst
# yay -S google-chrome-stable ranger visual-studio-code-bin gnome-keyring vlc ntp kdenlive zoom zsh neofetch docker bookworm  # Nice-to-haves
printf "Installing distrotube-st"
git clone https://gitlab.com/dwt1/st-distrotube.git
cd st-distrotube
sudo make clean install

printf "Applying rice\n"
mkdir -p ~/.config
sudo cp xinitrc ~/.xinitrc
sudo chmod 644 ~/.xinitrc
sudo chown root:root ~/.xinitrc
sudo cp -R config/qtile ~/.config/
chmod +x ~/.config/qtile/autostart.sh
sudo cp -R config/dunst ~/.config/

# Uncomment if installed ntp in nice to haves
# ntpd -u ntp:ntp
# sudo systemctl enable ntpd
# sudo systemctl start ntpd

# Uncomment if installed docker in nice to haves
# sudo sudo groupadd docker
# sudo groupadd docker
# sudo gpasswd -a $USER docker
# newgrp docker