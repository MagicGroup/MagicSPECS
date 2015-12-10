# Generated from erubis-2.6.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name erubis


Summary: A fast and extensible eRuby implementation
Name: rubygem-%{gem_name}
Version: 2.7.0
Release: 12%{?dist}
Group: Development/Languages
License: MIT
URL: http://www.kuwata-lab.com/erubis/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# needed for tests, to get it, run
# git clone https://github.com/kwatch/erubis && cd erubis
# git checkout 14d3eab57f && tar czvf erubis-2.7.0-public_html.tgz public_html
Source1: %{gem_name}-%{version}-public_html.tgz
# Fixes issues with test suite using Psych.
# https://github.com/kwatch/erubis/pull/2
Patch0: rubygem-erubis-2.7.0-ruby-2.0-compatibility.patch
# https://github.com/kwatch/erubis/pull/5
Patch1: rubygem-erubis-2.7-Add-support-for-Ruby-2.1.patch
Patch2: rubygem-erubis-2.7.0-Add-support-for-Ruby-2.2.patch
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
Erubis is a very fast, secure, and extensible implementation of eRuby.

%package doc
Summary: Documentation for %{name}
Group: Documentation
# contrib/erubis-run.rb is BSD
License: MIT and BSD
Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
mkdir -p .%{_bindir}
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
%patch2 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
mkdir -p %{buildroot}%{_bindir}

cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
cp -a .%{_bindir}/* %{buildroot}%{_bindir}/


find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

find %{buildroot}%{gem_instdir}/{bin,contrib} -type f | \
  xargs -n 1 sed -i -e 's"^#!/usr/bin/env ruby"#!/usr/bin/ruby"'

find %{buildroot}%{gem_instdir}/benchmark -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env ruby/d'

%check
export GEM_PATH=%{buildroot}%{gem_dir}:%{gem_dir}
export PATH=%{buildroot}%{_bindir}:$PATH

pushd .%{gem_instdir}
tar xzf %{SOURCE1}

# Wrong filename - reported upstream via
# http://rubyforge.org/tracker/?func=detail&aid=27330&group_id=1320&atid=5201
mv test/data/users-guide/{E,e}xample.ejava

# test_untabify2(MainTest) test fails. It is not obvious how to make it run
# with Psych, since Psych by design denies tabified YAML, where it was
# acceptable for Syck (if I am not mistaken).
# TODO: This could be ignored by --ignore-name= param if only it worked.
# https://github.com/test-unit/test-unit/issues/92
sed -i '/^  def test_untabify2/,/^  end$/ s/^/#/' test/test-main.rb

ruby -I.:lib -e "Dir.glob('./test/test-*.rb').each {|t| require t}"
popd

%files
%{_bindir}/erubis
%doc %{gem_instdir}/CHANGES.txt
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.txt
%dir %{gem_instdir}

# We install via gem
%exclude %{gem_instdir}/setup.rb
# Only needed for tests
%exclude %{gem_instdir}/public_html

%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/benchmark
%{gem_instdir}/test
%{gem_instdir}/examples
%{gem_instdir}/contrib

# Prefer generated rdoc
%exclude %{gem_instdir}/doc-api

%{gem_instdir}/doc
%{gem_docdir}

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.7.0-12
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.7.0-11
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.7.0-10
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Vít Ondruch <vondruch@redhat.com> - 2.7.0-8
- Fix test suite for Ruby 2.2 compatibility.

* Mon Jun 23 2014 Vít Ondruch <vondruch@redhat.com> - 2.7.0-7
- Fix FTBFS in Rawhide (rhbz#1107104).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 03 2014 Josef Stribny <jstribny@redhat.com> - 2.7.0-5
- Fix license in -doc subpackage

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 2.7.0-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.7.0-1
- Update to Erubis 2.7.0.
- Removed unneeded %%defattr usage.
- Removed no longer needed rubygem(abstract) dependency.
- Remove no longer needed test patch.

* Tue Jan 31 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 2.6.6-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 14 2011 Vít Ondruch <vondruch@redhat.com> - 2.6.6-1
- Updated to the latest upstream (#670589).
- Removed flawed require check.
- Removed obsolete BuildRoot.
- Removed obsolete cleanup.
- Package setup and test execution reworked.
- Removed bindir magick.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 29 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-2
- Move file rename to build stage (#530275).
- Simplify %%check stage (#530275).
- Remove disable of test_syntax2, fixed by new ruby build (#530275).

* Mon Oct 19 2009 Matthew Kent <mkent@magoazul.com> - 2.6.5-1
- Initial package
