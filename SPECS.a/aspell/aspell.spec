Summary: Spell checker
Summary(zh_CN.UTF-8): 拼写检查器
Name: aspell
Version: 0.60.6.1
Release: 4%{?dist}
Epoch: 12
# LGPLv2+ .. aspell-0.60.6/misc/po-filter.c, ltmain.sh, modules/speller/default/affix.cpp
# GPLv2+  .. aspell-0.60.6/misc/po-filter.c, aspell-0.60.6/ltmain.sh
# BSD     .. myspell/munch.c
License: LGPLv2 and LGPLv2+ and GPLv2+ and MIT
Group: Applications/Text
Group(zh_CN.UTF-8): 应用程序/文本
URL: http://aspell.net/
Source0: ftp://ftp.gnu.org/gnu/aspell/aspell-%{version}.tar.gz
Patch3: aspell-0.60.3-install_info.patch
Patch5: aspell-0.60.5-fileconflict.patch
Patch7: aspell-0.60.5-pspell_conf.patch
Patch8: aspell-0.60.6-zero.patch
Patch9: aspell-0.60.6-mp.patch
BuildRequires: gettext, ncurses-devel, pkgconfig
BuildRequires: chrpath
Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info

%description
GNU Aspell is a spell checker designed to eventually replace Ispell. It can
either be used as a library or as an independent spell checker. Its main
feature is that it does a much better job of coming up with possible
suggestions than just about any other spell checker out there for the
English language, including Ispell and Microsoft Word. It also has many
other technical enhancements over Ispell such as using shared memory for
dictionaries and intelligently handling personal dictionaries when more
than one Aspell process is open at once.

%description -l zh_CN.UTF-8
各种语言的拼写检查器。

%package	devel
Summary: Libraries and header files for Aspell development
Summary(zh_CN.UTF-8): %[name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: aspell = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description	devel
Aspell is a spelling checker. The aspell-devel package includes
libraries and header files needed for Aspell development.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n aspell-%{version}
%patch3 -p1 -b .iinfo
%patch5 -p1 -b .fc
%patch7 -p1 -b .mlib
%patch8 -p1 -b .zero
%patch9 -p1 -b .ai
iconv -f windows-1252 -t utf-8 manual/aspell.info -o manual/aspell.info.aux
mv manual/aspell.info.aux manual/aspell.info

%build
%configure --disable-rpath
make %{?_smp_mflags}
cp scripts/aspell-import examples/aspell-import
chmod 644 examples/aspell-import
cp manual/aspell-import.1 examples/aspell-import.1

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60

mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/ispell ${RPM_BUILD_ROOT}%{_bindir}
mv ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/spell ${RPM_BUILD_ROOT}%{_bindir}

chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//nroff-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//sgml-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//context-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//email-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//tex-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60//texinfo-filter.so
chrpath --delete ${RPM_BUILD_ROOT}%{_bindir}/aspell
chrpath --delete ${RPM_BUILD_ROOT}%{_libdir}/libpspell.so.*


rm -f ${RPM_BUILD_ROOT}%{_libdir}/libaspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libpspell.la
rm -f ${RPM_BUILD_ROOT}%{_libdir}/aspell-0.60/*-filter.la
rm -f ${RPM_BUILD_ROOT}%{_bindir}/aspell-import
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/aspell-import.1

%find_lang %{name}

%post
/sbin/ldconfig
if [ -f %{_infodir}/aspell.info.gz ]; then
    /sbin/install-info %{_infodir}/aspell.info.gz %{_infodir}/dir --entry="* Aspell: (aspell). "  || : 
fi

%post        devel
if [ -f %{_infodir}/aspell-dev.info.gz ]; then
    /sbin/install-info %{_infodir}/aspell-dev.info.gz %{_infodir}/dir --entry="* Aspell-dev: (aspell-dev). " || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/aspell.info.gz ]; then
        /sbin/install-info --delete %{_infodir}/aspell.info.gz %{_infodir}/dir || :
    fi
fi

%preun       devel
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/aspell-dev.info.gz ]; then
        /sbin/install-info --delete %{_infodir}/aspell-dev.info.gz %{_infodir}/dir || :
    fi
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README TODO COPYING examples/aspell-import examples/aspell-import.1
%dir %{_libdir}/aspell-0.60
%{_bindir}/a*
%{_bindir}/ispell
%{_bindir}/pr*
%{_bindir}/run-with-aspell
%{_bindir}/spell
%{_bindir}/word-list-compress
%{_libdir}/lib*.so.*
%{_libdir}/aspell-0.60/*
%{_infodir}/aspell.*
%{_mandir}/man1/aspell.1.*
%{_mandir}/man1/run-with-aspell.1*
%{_mandir}/man1/word-list-compress.1*
%{_mandir}/man1/prezip-bin.1.*

%files		devel
%defattr(-,root,root,-)
%dir %{_includedir}/pspell
%{_bindir}/pspell-config
%{_includedir}/aspell.h
%{_includedir}/pspell/pspell.h
%{_libdir}/lib*spell.so
%{_libdir}/pkgconfig/*
%{_infodir}/aspell-dev.*
%{_mandir}/man1/pspell-config.1*

%changelog
* Fri Sep 18 2015 Liu Di <liudidi@gmail.com> - 12:0.60.6.1-4
- 为 Magic 3.0 重建

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 12:0.60.6.1-2
- 为 Magic 3.0 重建

* Mon Oct 31 2011 Liu Di <liudidi@gmail.com> - 12:0.60.6.1-1
- 升级到 0.60.6.1

