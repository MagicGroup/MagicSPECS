# Generated from ZenTest-4.1.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ZenTest

Summary: Automated test scaffolding for Ruby
Name: rubygem-%{gem_name}
Version: 4.10.0
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/seattlerb/zentest
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
ZenTest is an automated test scaffolding for Ruby that provides 4 different
tools: zentest, unit_diff, autotest and multiruby. These tools can be used for
test conformance auditing and rapid XP.

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Various files marked executable that shouldn't be, and remove needless
# shebangs
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/local/bin/ruby"#!/usr/bin/ruby"'
find %{buildroot}%{gem_instdir}/test -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{gem_instdir} -type f | \
  xargs chmod 0644
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs chmod 0755

%check
pushd .%{gem_instdir}
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%{_bindir}/autotest
%{_bindir}/multigem
%{_bindir}/multiruby
%{_bindir}/multiruby_setup
%{_bindir}/unit_diff
%{_bindir}/zentest
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_instdir}/lib
%exclude %{gem_instdir}/.*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/test
%doc %{gem_instdir}/articles
%doc %{gem_instdir}/example*.rb
%doc %{gem_instdir}/example.txt

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 4.10.0-5
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 4.10.0-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 4.10.0-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 Vít Ondruch <vondruch@redhat.com> - 4.10.0-1
- Update to ZenTest 4.10.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Vít Ondruch <vondruch@redhat.com> - 4.9.0-2
- Rebuid due to error in RubyGems stub shebang.

* Tue Feb 19 2013 Vít Ondruch <vondruch@redhat.com> - 4.9.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to ZenTest 4.9.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 4.8.2-1
- update to zentest 4.8.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Vít Ondruch <vondruch@redhat.com> - 4.6.2-2
- Remove Rake dependency.

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 4.6.2-1
- 4.6.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Mo Morsi - 4.6.0-1
- New upstream version. Minor fixes and enhancements.

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 4.3.3-3
- Replace BR(check) with BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 26 2010 Matthew Kent <mkent@magoazul.com> - 4.3.3-1
- New upstream version. Minor fixes and enhancements.

* Tue May 4 2010 Matthew Kent <mkent@magoazul.com> - 4.3.1-1
- New upstream version. Minor bugfixes - 1.9 compatibility.

* Sun Jan 24 2010 Matthew Kent <mkent@magoazul.com> - 4.2.1-1
- New upstream version.
- Don't reorganize files, leave as upstream intended.

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-3
- Drop Requires on hoe, only used by Rakefile (#539442).
- Move Rakefile to -doc (#539442).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-2
- Better Source (#539442).
- More standard permissions on files.

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 4.1.4-1
- Initial package
