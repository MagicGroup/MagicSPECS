# Generated from pkg-config-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global	gem_name	pkg-config

%if 0%{?fedora} < 19
%global	rubyabi	1.9.1
%endif

Summary:	A pkg-config implementation by Ruby
Name:		rubygem-%{gem_name}
Version:	1.1.6
Release:	2%{?dist}
Group:		Development/Languages
License:	LGPLv2+
URL:		http://github.com/rcairo/pkg-config

Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Observe test failure on test_cflags test_cflags_only_I
# with pkgconfig 0.27
Patch0:	rubygem-pkg-config-1.1.3-cflags-result-sort.patch
# And yet another fix
Patch1:	rubygem-pkg-config-1.1.5-cflags-test-uniq.patch

%if 0%{?fedora} >= 19
Requires:	ruby(release)
BuildRequires:	ruby(release)
%else
Requires:	ruby(abi) = %{rubyabi}
Requires:	ruby 
BuildRequires:	ruby(abi) = %{rubyabi}
BuildRequires:	ruby 
%endif
BuildRequires:	rubygems-devel
# For %%check
#BuildRequires:	rubygem(rake)
#BuildRequires:	rubygem(hoe)
BuildRequires:	rubygem(test-unit)
# mkmf.rb requires ruby-devel
BuildRequires:	ruby-devel
BuildRequires:	cairo-devel
Requires:	rubygems

BuildArch:	noarch
Provides:	rubygem(%{gem_name}) = %{version}-%{release}

%description
This gem contains a pkg-config implementation by Ruby

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

%gem_install -n %{SOURCE0}

find . -name \*.gem | xargs chmod 0644

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
popd

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}/%{gem_dir}/

# Kill unneeded file
rm -f %{buildroot}%{gem_instdir}/extconf.rb

%clean
rm -rf %{buildroot}

%check
pushd .%{gem_instdir}
#rake test --verbose --trace
#ruby -Ilib -rubygems test/run-test.rb
cat > test.rb <<EOF
require "rubygems"
gem "test-unit"
require "test/unit"

Dir.glob("test/**/test_*.rb") do |file|
  require file
end
EOF
ruby -Ilib:test:. ./test.rb

%files
%defattr(-, root, root, -)
%dir	%{gem_instdir}
%doc	%{gem_instdir}/[A-Z]*
%exclude	%{gem_instdir}/Rakefile
%exclude	%{gem_instdir}/setup.rb
%{gem_libdir}/

%{gem_cache}
%{gem_spec}

%files	doc
%defattr(-,root,root,-)
%{gem_instdir}/test/
%{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.6-1
- 1.1.6

* Thu Jun 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.5-3
- Fix build failure

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 31 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.5-1
- 1.1.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.4-3
- F-19: Rebuild for ruby 2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.4-1
- 1.1.4

* Thu Aug  2 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-3
- Fix test failure on test_cflags, test_cflags_only_I with
  recent pkgconfig

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.3-1
- 1.1.3

* Sun Jan 29 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-3
- F-17: rebuild against ruby 1.9

* Sun Jan 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org>
- Fix test failure with new png

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- F-17: Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-1
- 1.1.2

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.7-2
- F-15 mass rebuild

* Thu Oct  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.7-1
- 1.0.7

* Thu Sep 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.6-2
- Add R: rubygems

* Thu Sep 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.6-1
- 1.0.6

* Fri Sep 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.3-1
- Initial package
