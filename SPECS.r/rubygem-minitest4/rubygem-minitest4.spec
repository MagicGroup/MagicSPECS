%global	gem_name minitest
# Use full EVR for provides
%global	__provides_exclude_from	%{gem_spec}

Summary:	Small and fast replacement for ruby's huge and slow test/unit

Name:		rubygem-%{gem_name}4
# With 4.7.5, some test fails, so for now use 4.7.0
Version:	4.7.0
Release:	5%{?dist}

License:	MIT
URL:		https://github.com/seattlerb/minitest
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires:	rubygems-devel
BuildRequires:	ruby(release)
BuildArch:			noarch
Provides:			rubygem(%{gem_name}) = %{version}-%{release}
# Also provide this
Provides:			rubygem(%{gem_name}4) = %{version}-%{release}
Conflicts:			rubygem-minitest < 4.7.0-3

%description
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular
test writer and for language implementors that need a minimal set of
methods to bootstrap a working unit test suite.

miniunit/spec is a functionally complete spec engine.

miniunit/mock, by Steven Baker, is a beautifully tiny mock object framework.

This is a compatibitity package for minitest version 4.x.y.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

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

find %{buildroot}%{gem_instdir}/lib -type f | \
	xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/ruby.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{gem_instdir} -type f | \
	xargs chmod 0644

# Cleanup
rm -f %{buildroot}%{gem_instdir}/{.autotest,.gemtest}
rm -f %{buildroot}%{gem_cache}
rm -rf %{buildroot}%{gem_instdir}/{Rakefile,test/}

%check
pushd .%{gem_instdir}

# spec test suite is unstable.
# https://github.com/seattlerb/minitest/issues/257
mv test/minitest/test_minitest_spec.rb{,.ignore}

for f in test/minitest/test_*.rb
do
	ruby -Ilib:.:./test $f
done

%files
%doc	%{gem_instdir}/History.txt
%doc	%{gem_instdir}/Manifest.txt
%license	%{gem_instdir}/README.txt
%dir	%{gem_instdir}
%{gem_libdir}/
%{gem_spec}

%files doc
%{gem_instdir}/design_rationale.rb
%doc	%{gem_docdir}/

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-4
- rpmlint fix
- Filter out redundant Provides
- Add Conflicts for older rubygem-minitest

* Mon Jun  9 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-3
- Rename to rubygem-minitest4
- Bump release number

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Josef Stribny <jstribny@redhat.com> - 4.7.0-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to minitest 4.7.0.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.10.1-1
- 2.10.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.6.0-3
- Removed Rake circular dependency.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-1
- Update to 1.6.0 (#586505)
- Patch0 removed

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-3
- Drop Requires on hoe, only used by Rakefile (#538303).
- Move Rakefile to -doc (#538303).

* Sat Nov 21 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-2
- Better Source (#538303).
- More standard permissions on files.

* Tue Nov 17 2009 Matthew Kent <mkent@magoazul.com> - 1.4.2-1
- Initial package
