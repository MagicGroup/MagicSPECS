%global svndate 20120510

Name:           mtpfs
Version:        1.1
Release:        0.4.svn%{svndate}%{?dist}
Summary:        FUSE file system allowing MTP device to be mounted and browsed

License:        GPLv3
URL:            https://code.google.com/p/mtpfs/

# Upstream mtpfs does not have releases, so I created this tarball
# directly from SVN.  Here's how:
#   svn checkout http://mtpfs.googlecode.com/svn/trunk/ mtpfs-read-only
#   rm -rf mtpfs-read-only/.svn
#   tar zcf mtpfs-%{svndate}.tar.gz mtpfs-read-only/

Source0:        mtpfs-%{svndate}.tar.gz

# autotools are required to build from SVN.
BuildRequires:  autoconf, automake

BuildRequires:  libid3tag-devel
BuildRequires:  fuse-devel
BuildRequires:  libmtp-devel
BuildRequires:  glib2-devel
# configure could use this, but libmad-devel is missing and libmad
# seems not to have a pkgconfig file.
#BuildRequires:  libmad

# Not strictly required, but hard to see how it's useful without it.
Requires:       %{_bindir}/fusermount


%description
MTPFS is a FUSE file system based on libmtp that allows an MTP device
to be browsed as if it were a normal external hard disk.

You can use this to mount and browse some Android tablet computers.


%prep
%setup -q -n mtpfs-read-only


%build
autoreconf -i
%configure --disable-mad
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/mtpfs


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.1-0.4.svn20120510
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.3.svn20120510
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-0.2.svn20120510
- Use _bindir instead of hard-coding path.
- Drop buildroot removal from install section.
- filesystem -> file system (ugh)

* Thu May 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-0.1.svn20120510
- Initial release for Fedora.
