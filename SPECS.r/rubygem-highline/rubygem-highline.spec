# Generated from highline-1.6.11.gem by gem2rpm -*- rpm-spec -*-
%global gem_name highline

Summary: HighLine is a high-level command-line IO library
Name: rubygem-%{gem_name}
Version: 1.6.21
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2 or Ruby or BSD
URL: https://github.com/JEG2/highline
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
A high-level IO library that provides validation, type conversion, and more
for command-line interfaces. HighLine also includes a complete menu system
that can crank out anything from simple list selection to complete shells
with just minutes of work.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Fix the shebang.
find %{buildroot}%{gem_instdir}/{examples,lib,test}/ -type f -name '*.rb' -exec \
    sed -i -e 's|/usr/local/bin/ruby|/usr/bin/ruby|' '{}' \;

# Remove hidden files.
find %{buildroot}%{gem_instdir}/ -type f -iname '.*' -exec rm -f '{}' \;


%check
pushd .%{gem_instdir}
# Test fails without real terminal.
sed -i '/^  def test_terminal_size$/,/^  end$/ s/^/#/' test/tc_highline.rb

# Set locales, since the test suite does some unjustified assumptions about
# encoding.
# https://github.com/JEG2/highline/issues/108
LANG=en_US.utf8 ruby -Ilib:test test/ts_all.rb
popd

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/setup.rb
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/COPYING

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/TODO
%doc %{gem_instdir}/CHANGELOG
%doc %{gem_instdir}/LICENSE
%{gem_instdir}/AUTHORS
%{gem_instdir}/Rakefile
%{gem_instdir}/examples
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/site
%{gem_instdir}/test
%exclude %{gem_instdir}/INSTALL

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jul 09 2014 Vít Ondruch <vondruch@redhat.com> - 1.6.21-1
- Update to HighLine 1.6.21.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.6.11-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk>  - 1.6.11-2
- add spec template
- remove INSTALL file

* Mon Feb 27 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk>  - 1.6.11-1
- update to upstream release 1.6.11

* Wed Feb 22 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 1.5.2-1
- update to upstream release 1.5.2
- remove obsolete BuildRoot tag, %%clean section and %%defattr

* Thu Feb 02 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.5.1-4
- Rebuilt for Ruby 1.9.3.
- Introduced -doc subpackage.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.5.1-1
- New upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.5.0-1
- New upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 1.4.0-2
- Add ruby(abi) = 1.8 requires

* Sun Jul 13 2008 root <root@oss1-repo.usersys.redhat.com> - 1.4.0-1
- Initial package
