%global	gem_name	rabbit
%define	BothRequires() \
Requires:	%1 \
BuildRequires:	%1 \
%{nil}

Name:		rubygem-%{gem_name}
Version:	2.1.8
Release:	3%{?dist}

Summary:	RD-document-based presentation application
# CC-BY: rubykaigi2011-background-white.jpg and
# rubykaigi2011-background-black.jpg
# (see doc/en/index.rd)
License:	GPLv2+ and CC-BY
URL:		http://rabbit-shocker.org/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rabbit-shocker/rabbit.git
# cd rabbit/
# git reset --hard %%{version}
# tar czf rubygem-rabbit-%%{version}-test-missing-files.tar.gz test/fixtures/
Source1:	%{name}-2.1.2-test-missing-files.tar.gz
Source10:	rabbit.desktop
Source11:	rabbit.xml

%BothRequires	ruby(release)
BuildRequires:	rubygems-devel
Requires:	ruby(rubygems)

%BothRequires	rubygem(coderay)
%BothRequires	rubygem(faraday)
%BothRequires	rubygem(gettext)
%BothRequires	rubygem(gtk2)
%BothRequires	rubygem(gio2)
%BothRequires	rubygem(hikidoc)
%BothRequires	rubygem(kramdown)
%BothRequires	rubygem(nokogiri)
%BothRequires	rubygem(poppler)
%BothRequires	rubygem(rsvg2)
%BothRequires	rubygem(rdtool)
%BothRequires	rubygem(rttool)
# test_codeblock_fence test needs below
BuildRequires:	%{_bindir}/blockdiag
BuildRequires:	desktop-file-utils
# For rabbirc
Requires:	rubygem(net-irc)

BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	rubygem(test-unit-rr)
BuildRequires:	xorg-x11-server-Xvfb

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}

%description
Rabbit is an RD-document-based presentation application.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
	%{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Desktop, mime, icon
mkdir -p -m 0755 \
	%{buildroot}%{_datadir}/{applications/,mime/packages/}
desktop-file-install \
	--dir=%{buildroot}%{_datadir}/applications/ \
	%{SOURCE10}
install -cpm 644 %{SOURCE11} %{buildroot}%{_datadir}/mime/packages/

mkdir -p -m 0755 \
	%{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
install -cpm 644 .%{gem_instdir}/sample/rabbit_icon.png \
	%{buildroot}%{_datadir}/icons/hicolor/32x32/apps/

# Cleanup
pushd %{buildroot}%{gem_instdir}
rm -rf \
	Gemfile Rakefile %{gem_name}.gemspec \
	po/ \
	test/
popd

%find_lang rabbit
# list directories under %%{gem_instdir}/data/locale/
find %{buildroot}%{gem_instdir}/data/locale -type d | while read dir
do
	echo "%%dir ${dir#%{buildroot}}" >> rabbit.lang
done

%check
# test files are not included in binary rpm, so just
# unpack here
pushd .%{gem_instdir}
gzip -dc %{SOURCE1} | tar -xf -
xvfb-run \
	ruby test/run-test.rb
popd

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f rabbit.lang
# rpmlint: keep all zero-length file
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*

%{_bindir}/rabbit-slide
%{_bindir}/rabbit
%{_bindir}/rabbit-theme
%{_bindir}/rabbit-command
%{_bindir}/rabbirc
%{gem_instdir}/bin

%{gem_libdir}
%dir	%{gem_instdir}/data/
%{gem_instdir}/data/account.kou.gpg
%{gem_instdir}/data/rabbit/
%{gem_instdir}/entities/

%{_datadir}/applications/rabbit.desktop
%{_datadir}/mime/packages/rabbit.xml
%{_datadir}/icons/hicolor/32x32/apps/rabbit_icon.png

%exclude	%{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/doc/
%dir	%{gem_instdir}/misc/
%{gem_instdir}/misc/*.rb
%doc	%{gem_instdir}/misc/*/
%doc	%{gem_instdir}/sample/	

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.1.8-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.1.8-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.8-1
- 2.1.8

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 27 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.6-1
- 2.1.6

* Tue Feb 24 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.4-1
- 2.1.4

* Fri Nov  7 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.3-3
- Rescue Encoding::UndefinedConversionError on logger
  (shocker-ja:1228)

* Thu Oct 02 2014 Rex Dieter <rdieter@fedoraproject.org> 2.1.3-2
- update desktop/icon/mime scriptlets

* Wed Aug 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.3-1
- 2.1.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.2-2
- Always call xvfb-run at %%check

* Mon Mar 17 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.2-1
- 2.1.2

* Mon Dec 23 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.1-3
- Use xvfb-run on F-19

* Mon Dec 23 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.1-2
- Require net-irc for rabbirc
- Install desktop and mime, icon

* Sun Nov 17 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.1.1-1
- Initial package
