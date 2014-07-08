Name:           lzip
Version:        1.15
Release:        2%{?dist}
Summary:        LZMA compressor with integrity checking
Summary(zh_CN.UTF-8): 带校验的 LZMA 压缩器

Group:          Applications/File
Group(zh_CN.UTF-8): 应用程序/文件
License:        GPLv3+
URL:            http://www.nongnu.org/lzip/lzip.html
Source0:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
Source1:        http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz.sig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): info
Requires(preun): info

%description
Lzip compresses data using LZMA (Lempel-Ziv-Markov chain-Algorithm). It
supports integrity checking using CRC (Cyclic Redundancy Check). To archive
multiple files, tar can be used with lzip. Please note, that the lzip file
format (.lz) is not compatible with the lzma file format (.lzma).

%description -l zh_CN.UTF-8
带校验的 LZMA 压缩器。

%prep
%setup -q
# file needs to be copied, because it is used in "make check"
cp -a COPYING{,.txt}
# convert CRLF to LF
sed -i 's/\r//' COPYING.txt 


%build
%configure CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" CPPFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install install-man DESTDIR=$RPM_BUILD_ROOT

# if install-info is present, this is created by upstream's makefile
rm -Rf $RPM_BUILD_ROOT%{_infodir}/dir
magic_rpm_clean.sh

%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :


%preun
if [ $1 = 0 ] ; then
/sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi


%files
%defattr(-,root,root,-)
# TODO is currently empty
%doc AUTHORS ChangeLog COPYING.txt NEWS README
%{_bindir}/lzip
#%%{_bindir}/lziprecover
%{_infodir}/lzip.info*
%{_mandir}/man1/lzip.1*
#%%{_mandir}/man1/lziprecover.1*


%changelog
* Tue Jul 08 2014 Liu Di <liudidi@gmail.com> - 1.15-2
- 为 Magic 3.0 重建

* Tue Oct 01 2013 Jon Ciesla <limburgher@gmail.com> - 1.15-1
- New upstream, 1014165.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 06 2013 Jon Ciesla <limburgher@gmail.com> - 1.14-1
- New upstream, 918416.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Jon Ciesla <limburgher@gmail.com> - 1.13-1
- New upstream, BZ 802973.
- lziprecover is now separate.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 05 2011 Jon Ciesla <limb@jcomserv.net> - 1.12-1
- Update to new release, BZ 702309.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 04 2010 Jon Ciesla <limb@jcomserv.net> - 1.11-1
- Update to new release, BZ 639555.

* Mon Jun 28 2010 Jon Ciesla <limb@jcomserv.net> - 1.10-1
- Update to new release, BZ 556767.

* Thu Dec 31 2009 Till Maas <opensource@till.name> - 1.8-1
- Update to new release
- Fix end of line encoding of COPYING

* Fri Aug 07 2009 Till Maas <opensource@till.name> - 1.7-2
- Exclude lzdiff & lzgrep, they will become part of zutils:
  http://www.nongnu.org/lzip/zutils.html
  and fixes a conflict with xz-lzma-compat: Red Hat Bugzilla #515502
- Use globbing for all manpages

* Tue Jul 28 2009 Till Maas <opensource@till.name> - 1.7-1
- Update to latest stable upstream
- remove upstreamed patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Till Maas <opensource@till.name> - 1.4-1
- Update to new release
- Add compile fixes for gcc 4.4 (missing #include <cstdio.h>)

* Thu Nov 27 2008 Till Maas <opensource@till.name> - 1.1-2
- fix type in summary
- call testsuite in %%check
- remove empty TODO file from %%doc

* Wed Nov 26 2008 Till Maas <opensource@till.name> - 1.1-1
- Initial spec for Fedora
