Summary:	Portable Musepack encoder
Summary(zh_CN.UTF-8): 可移植 Musepack 编码器
Name:		mppenc
Version:		1.16
Release:	6%{?dist}
License:		LGPL
Group:		Applications/Multimedia
Group(zh_CN.UTF-8):	应用程序/多媒体
Source0:	http://files.musepack.net/source/mppenc-%{version}.tar.bz2
URL:		http://www.musepack.net/
BuildRequires:	nasm
BuildRequires:	cmake >= 2.2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%description
Portable Musepack encoder

%description -l zh_CN.UTF-8
Mppenc 是可移植的 Musepack 编码器，提供对 MPC 音频格式的编码功能。
MPC 音频格式是一个高品质、低损耗的音频压缩编码格式。在同一个音频源文件
产生相似体积的 MPC 和 MP3 文件的情况下，MPC 文件的质量要较 MP3 文件
好得多；在相似质量情况下，MPC 格式文件的体积要较 MP3 格式文件的体积小
得多。

%prep
%setup -q

%build
cmake -DCMAKE_INSTALL_PREFIX:=%{_prefix} .
make
	    
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot} %{_builddir}/%{buildsubdir}

%files
%defattr(644,root,root,755)
%doc Changelog
%attr(755,root,root) %{_bindir}/*


%changelog
* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 1.16-6
- 为 Magic 3.0 重建

* Thu Jan 01 2015 Liu Di <liudidi@gmail.com> - 1.16-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.16-4
- 为 Magic 3.0 重建

* Wed Jan 18 2012 Liu Di <liudidi@gmail.com> - 1.16-3
- 为 Magic 3.0 重建

* Tue May 29 2007 kde <athena_star {at} 163 {dot} com> - 1.1.6
- initial package
