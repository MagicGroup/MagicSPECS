Name:		AcetoneISO2
Version:	2.3
Release:	4%{?dist}
Summary:	CD/DVD Image Manipulator
Summary(zh_CN): CD/DVD 镜像管理
Group:		Applications/Archiving
Group(zh_CN):	应用程序/归档
License:	GPLv3
URL:		http://www.acetoneteam.org/
Source0:	http://download.sourceforge.net/sourceforge/acetoneiso2/acetoneiso_%{version}.tar.gz
Patch1:		AcetoneISO2-2.0.3-no-poweriso-for-non-x86.patch
Patch2:		acetoneiso_2.3-phonon.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	kdewebdev4-devel, qt4-devel, desktop-file-utils
BuildRequires:	phonon-devel
Requires:	p7zip, cdrdao
Requires:	fuseiso, fuse, genisoimage
Requires:	gnupg, pinentry-qt
# Overkill, but I'm being thorough
Requires:	util-linux, coreutils

%description
AcetoneISO2: The CD/DVD image manipulator for Linux, it can do the following:
- Mount and Unmount ISO, MDF, NRG (if iso-9660 standard)
- Convert / Extract / Browse to ISO : *.bin *.mdf *.nrg *.img *.daa *.cdi 
  *.xbx *.b5i *.bwi *.pdi
- Play a DVD Movie ISO with most commonly-used media players
- Generate an ISO from a Folder or CD/DVD
- Generate/Check MD5 file of an image
- Encrypt/decrypt an image
- Split image into X megabyte chunks
- Highly compress an image
- Rip a PSX cd to *.bin to make it work with epsxe/psx emulators
- Restore a lost CUE file of *.bin *.img

%description -l zh_CN
CD/DVD 镜像管理

%prep
%setup -q -n acetoneiso_%{version}
%patch1 -p1
%patch2 -p1

%build
cd acetoneiso
qmake-qt4 "QMAKE_CXXFLAGS=$RPM_OPT_FLAGS -I/opt/kde4/include/KDE"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT 
cd acetoneiso
make INSTALL_ROOT=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT%{_datadir}/applications/AcetoneISO.desktop $RPM_BUILD_ROOT%{_datadir}/applications/AcetoneISO2.desktop
mv $RPM_BUILD_ROOT%{_bindir}/acetoneiso $RPM_BUILD_ROOT%{_bindir}/acetoneiso2

sed -i 's|Exec=acetoneiso|Exec=acetoneiso2|g' $RPM_BUILD_ROOT%{_datadir}/applications/AcetoneISO2.desktop

desktop-file-install --vendor ""			\
	--dir $RPM_BUILD_ROOT%{_datadir}/applications	\
	--add-category System				\
	$RPM_BUILD_ROOT%{_datadir}/applications/AcetoneISO2.desktop

%clean
rm -rf $RPM_BUILD_ROOT 

%files
%defattr(-,root,root)
%doc AUTHORS CHANGELOG FEATURES LICENSE README
%{_bindir}/acetoneiso2
# %%{_datadir}/acetoneiso2
%{_datadir}/applications/AcetoneISO2.desktop
%{_datadir}/pixmaps/Acetino2.png

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 2.3-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 2.3-3
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 2.3-2
- 为 Magic 3.0 重建

* Sun Oct 30 2011 Liu Di <liudidi@gmail.com> - 2.3-1
- 升级到 2.3
