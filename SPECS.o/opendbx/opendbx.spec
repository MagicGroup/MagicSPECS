Name:           opendbx
Version:        1.4.6
Release:        8%{?dist}
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Lightweight but extensible database access library written in C
Summary(zh_CN.UTF-8): 使用 C 编写的轻量级但是可扩展的数据库访问库

#License:        LGPLv2+
# (util/argmap.{cpp,hpp}) have a GPL license header rather than an LGPL one
# until upstream decides about this I am leaving GPLv2+ here as the stricter license
License:        GPLv2+
URL:            http://www.linuxnetworks.de/doc/index.php/OpenDBX
Source0:        http://linuxnetworks.de/opendbx/download/%{name}-%{version}.tar.gz
Patch0:         opendbx-1.4.6-freetds-fix.patch
Patch1:         opendbx-1.4.6-doxyfile-fix.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mysql-devel, postgresql-devel, sqlite2-devel, sqlite-devel, firebird-devel, readline-devel
BuildRequires:  freetds-devel, ncurses-devel
BuildRequires:  doxygen, docbook2X, gettext

%{?filter_setup:
%filter_provides_in %{_libdir}/opendbx/lib.*backend\.so.*$
%filter_requires_in %{_libdir}/opendbx/lib.*backend\.so.*$
%filter_setup
}

%description
Provides an abstraction layer to all supported databases with a single, clean
and simple interface that leads to an elegant code design automatically.
If you want your application to support different databases with little effort,
this is definitively the right thing for you!

%description -l zh_CN.UTF-8
使用 C 编写的轻量级但是可扩展的数据库访问库。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        mysql
Summary:        MySQL backend - provides mysql support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    mysql
Allows odbx_init with "mysql" as the backend parameter.

%package        postgresql
Summary:        PostgreSQL backend - provides postgresql support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    postgresql
Allows odbx_init with "pgsql" as the backend parameter.

%package        sqlite2
Summary:        SQLite 2 backend - provides sqlite2 support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    sqlite2
Allows odbx_init with "sqlite" as the backend parameter.

%package        sqlite
Summary:        SQLite 3 backend - provides sqlite3 support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    sqlite
Allows odbx_init with "sqlite3" as the backend parameter.

%package        firebird
Summary:        Firebird backend - provides firebird support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    firebird
Allows odbx_init with "firebird" as the backend parameter.

%package        mssql
Summary:        MSSQL backend - provides mssql support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    mssql
Allows odbx_init with "mssql" as the backend parameter.

%package        sybase
Summary:        Sybase backend - provides sybase support in %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    sybase
Allows odbx_init with "sybase" as the backend parameter.

%package        utils
Summary:        Utility binaries for %{name}
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    utils
The %{name}-utils package provides the odbx-sql tool.

%prep
%setup -q
%patch0 -p1 -b .freetds
%patch1 -p1 -b .doxyfile

# To fix Doxygen parsing issue
ln -s api lib/%{name}/api.dox

%build
%configure --with-backends="mysql pgsql sqlite sqlite3 firebird mssql sybase" CPPFLAGS="-I%{_includedir}/mysql" --disable-test --disable-static LDFLAGS="-L%{_libdir}/mysql"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%find_lang %{name}
%find_lang %{name}-utils

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %{_libdir}/opendbx
%{_libdir}/*.so.*
%{_datadir}/opendbx/keywords

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.gz

%files mysql
%{_libdir}/opendbx/*mysql*.so
%{_libdir}/opendbx/*mysql*.so.*

%files postgresql
%{_libdir}/opendbx/*pgsql*.so
%{_libdir}/opendbx/*pgsql*.so.*

%files sqlite2
%{_libdir}/opendbx/*sqlitebackend.so
%{_libdir}/opendbx/*sqlitebackend.so.*

%files sqlite
%{_libdir}/opendbx/*sqlite3backend.so
%{_libdir}/opendbx/*sqlite3backend.so.*

%files firebird
%{_libdir}/opendbx/*firebird*.so
%{_libdir}/opendbx/*firebird*.so.*

%files mssql
%{_libdir}/opendbx/*mssql*.so
%{_libdir}/opendbx/*mssql*.so.*

%files sybase
%{_libdir}/opendbx/*sybase*.so
%{_libdir}/opendbx/*sybase*.so.*

%files utils -f %{name}-utils.lang
%{_bindir}/odbx-sql
%{_mandir}/man1/odbx-sql.1.gz

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.6-8
- 为 Magic 3.0 重建

* Thu Apr 16 2015 Liu Di <liudidi@gmail.com> - 1.4.6-7
- 为 Magic 3.0 重建

* Fri Apr 03 2015 Steve Jenkins <steve@stevejenkins.com> - 1.4.6-6
- Removing percentage sign from 1.4.6-5 comments; it made EL6 choke

* Fri Apr 03 2015 Steve Jenkins <steve@stevejenkins.com> - 1.4.6-5
- Applied patch for Doxyfile.in issue (similar to Debian bug #759951)
- Create symlink in prep to work around doxygen issue (Bugzilla #1208902)

* Thu Apr 02 2015 Steve Jenkins <steve@stevejenkins.com> - 1.4.6-4
- Added Group: info for package and sub-packages (for EL5 and EL6)
- Added ncurses-devel to BuildRequires (for EL5)
- Added BuildRoot (for EL5)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.6-1
- Update to 1.4.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-8
- Rebuilt for c++ ABI breakage

* Wed Jan 18 2012 Martin Preisler <mpreisle@redhat.com> 1.4.5-7
- fixed compile error caused by freetds API break via a patch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 19 2011 Martin Preisler <mpreisle@redhat.com> 1.4.5-5
- also filter requires for the backend packages

* Mon Oct 17 2011 Martin Preisler <mpreisle@redhat.com> 1.4.5-4
- only the base package owns {_libdir}/opendbx now

* Wed Oct 12 2011 Martin Preisler <mpreisle@redhat.com> 1.4.5-3
- the backends now explicity require opendbx of the same version
- filter out provides of backend subpackages
- use GPLv2+ as license for now because of the 2 GPLv2+ files

* Tue Sep 20 2011 Martin Preisler <mpreisle@redhat.com> 1.4.5-2
- added mysql, postgresql, sqlite2, sqlite3, firebird, mssql, sybase backends
- moved readline dependency to utils subpackage

* Mon Sep 19 2011 Martin Preisler <mpreisle@redhat.com> 1.4.5-1
- initial package
