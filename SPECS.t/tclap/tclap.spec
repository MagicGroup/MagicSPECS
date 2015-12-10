Name:           tclap
Summary:        Template-Only Command Line Argument Parser
Summary(zh_CN.UTF-8): 只有模板的命令行参数解析器
Version:	1.2.1
Release:	3%{?dist}
License:        MIT
URL:            http://%{name}.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
%{name} is a small, flexible library that provides a simple interface for 
defining and accessing command line arguments. It was initially inspired by
the user friendly CLAP library. The difference is that this library is
template-only, so the argument class is type independent. Type independence 
avoids identical-except-for-type objects, such as IntArg, FloatArg, and
StringArg. While the library is not strictly compliant with the GNU or
POSIX standards, it is close.

%{name} is written in ANSI C++ and is meant to be compatible with any
standards-compliant C++ compiler. The library is implemented entirely
in header files making it easy to use and distribute with other software.

It implies that this package is almost empty. The actual content, i.e.,
the header files, are provided by the development package.

%{name} is now a mature, stable, and feature rich package. It probably will not
see much further development aside from bug fixes and compatibility updates.

%description -l zh_CN.UTF-8
只有模板的命令行参数解析器。

%package devel
Summary:        Header files for the Template-Only Command Line Argument Parser
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Headers for the Template-Only Command Line Argument Parser.
Note: as that project has only headers (i.e., no library/binary object),
this package (i.e., the -devel package) is the one containing most of the 
project.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package doc
Summary:        API Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildRequires:  doxygen, graphviz

%description doc
API documentation for the Template-Only Command Line Argument Parser library

%description doc -l zh_CN.UTF-8
%{name} 的开发文档。

%prep
%setup -q
sed -i 's/\r//' docs/style.css

%build
%configure
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Move the pkgconfig helper file to the right location for Fedora
# when the package is noarch
mv -f %{buildroot}%{_libdir}/pkgconfig/ %{buildroot}%{_datadir}/
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_datadir}/pkgconfig/%{name}.pc
%doc AUTHORS COPYING README

%files doc
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_defaultdocdir}/%{name}/

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.2.1-3
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.1-2
- 为 Magic 3.0 重建

* Wed Sep 30 2015 Liu Di <liudidi@gmail.com> - 1.2.1-1
- 更新到 1.2.1

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.2.0-5
- 为 Magic 3.0 重建

* Wed Oct 05 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> 1.2.0-4
- The package and sub-packages are now all noarch.
- A few cosmetic improvements have also been made.

* Thu Jul 28 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> 1.2.0-3
- Re-added a main package, almost empty

* Mon Jul 04 2011 Bruno Postle 1.2.0-2
- create -devel package without a base package

* Tue Mar 08 2011 Bruno Postle 1.2.0-1
- initial fedora package

