%define name	libmpcdec
%define version	1.2.6
%define release	5%{?dist}

Name: 	%{name}
Summary: 	Portable Musepack decoder library
Summary(zh_CN.UTF-8): 可移植 Musepack 解码器库
Version: 	%{version}
Release: 	%{release}.1

Source:	http://files.musepack.net/source/%{name}-%{version}.tar.bz2
URL:		http://www.musepack.net
License:	BSD
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
Portable Musepack decoder library.

%description -l zh_CN.UTF-8
Libmpcdec 是可移植的 Musepack 解码器库，提供对 MPC 音频格式的解码功能。
MPC 音频格式是一个高品质、低损耗的音频压缩编码格式。在同一个音频源文件
产生相似体积的 MPC 和 MP3 文件的情况下，MPC 文件的质量要较 MP3 文件
好得多；在相似质量情况下，MPC 格式文件的体积要较 MP3 格式文件的体积小
得多。

%package	devel
Summary: 	Header files and static libraries from %{name}
Summary(zh_CN.UTF-8): %{name} 的头文件和静态库
Group:		Development/Libraries
Group(zh_CN.UTF-8):	开发/库
Requires: 	%{name} >= %{version}

%description devel
Libraries and includes files for developing programs based on %{name}.

%description -l zh_CN.UTF-8 devel
Libmpcdec 是可移植的 Musepack 解码器库，提供对 MPC 音频格式的解码功能。
这是开发基于 %{name} 的程序的头文件和静态库。


%prep
%setup -q

%build
%configure

%{__make} %{?_smp_mflags}
										
%install
rm -rf %{buildroot}

%makeinstall
magic_rpm_clean.sh

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc AUTHORS README ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/*.la


%changelog
* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 1.2.6-5.1
- 为 Magic 3.0 重建

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.2.6-4
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Liu Di <liudidi@gmail.com> - 1.2.6-3
- 为 Magic 3.0 重建

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 1.2.6
- initial package
