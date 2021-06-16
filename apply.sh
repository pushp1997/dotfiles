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
yay -S xorg xorg-xinit qtile alacritty feh scrot betterlockscreen udiskie ntfs-3g ttf-font-awesome ttc-iosevka picom htop harfbuzz ttf-hack-nerd ttf-joypixels brightnessctl network-manager-applet ttf-ubuntu-font-family dunst
# yay -S google-chrome-stable ranger visual-studio-code-bin gnome-keyring vlc ntp kdenlive zoom zsh neofetch docker bookworm  # Nice-to-haves

printf "Applying rice\n"
mkdir -p ~/.config
sudo cp xinitrc ~/.xinitrc
sudo chmod 644 ~/.xinitrc
sudo chown root:root ~/.xinitrc
sudo cp -R config/qtile ~/.config/
chmod +x ~/.config/qtile/autostart.sh
sudo cp -R config/dunst ~/.config/
sudo cat synaptics.conf >> /usr/share/X11/xorg.conf.d/70-synaptics.conf

# Uncomment for i3wm
# sudo cp config/i3/config ~/.config/i3/config && sudo chown pushp:users ~/.config/i3/config
# sudo cp config/i3status/i3status.conf ~/.config/i3status/i3status.conf && sudo chown pushp:users ~/.config/i3status/i3status.conf

# Uncomment if installed ntp in nice to haves
# ntpd -u ntp:ntp
# sudo systemctl enable ntpd
# sudo systemctl start ntpd

# Uncomment if installed docker in nice to haves
# sudo sudo groupadd docker
# sudo groupadd docker
# sudo gpasswd -a $USER docker
# newgrp docker

printf "Rice Applied!\nYou can now run startx"