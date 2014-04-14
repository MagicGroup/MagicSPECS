Summary: The GNU chess program
Summary(zh_CN): GNU 国际象棋程序
Name: gnuchess
Version:	6.1.1
Release: 2%{?dist}
License: GPLv2+
Group: Amusements/Games
Group(zh_CN): 娱乐/游戏
URL: ftp://ftp.gnu.org/pub/gnu/chess/
Source: ftp://ftp.gnu.org/pub/gnu/chess/%{name}-%{version}.tar.gz
#Source1: http://ftp.gnu.org/pub/gnu/chess/book_1.01.pgn.gz
# use precompiled book.dat:
Source1: book_1.01.dat.gz
Patch1: gnuchess-5.06-bookpath.patch
Patch2: gnuchess-5.07-getline.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: chessprogram
BuildRequires: flex

%description
The gnuchess package contains the GNU chess program.  By default,
GNU chess uses a curses text-based interface.  Alternatively, GNU chess
can be used in conjunction with the xboard user interface and the X
Window System for play using a graphical chess board.

Install the gnuchess package if you would like to play chess on your
computer.  If you'd like to use a graphical interface with GNU chess, 
you'll also need to install the xboard package and the X Window System.

%description -l zh_CN
GNU 国际象棋程序。

%prep
%setup -q -n %{name}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/games/gnuchess $RPM_BUILD_ROOT%{_bindir}
install -m 755 -p src/gnuchess $RPM_BUILD_ROOT%{_bindir}
#install -m 644 -p book/book.dat $RPM_BUILD_ROOT%{_var}/lib/games/gnuchess
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(2755,root,games) %{_bindir}/gnuchess
%dir %{_var}/lib/games/gnuchess
#%attr(664,root,games) %{_var}/lib/games/gnuchess/book.dat
%doc doc/* COPYING AUTHORS NEWS TODO 

%changelog
* Fri Apr 11 2014 Liu Di <liudidi@gmail.com> - 6.1.1-2
- 更新到 6.1.1

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 6.0.1-2
- 为 Magic 3.0 重建


