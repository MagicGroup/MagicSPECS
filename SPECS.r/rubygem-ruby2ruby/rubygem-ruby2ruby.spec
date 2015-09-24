# Generated from ruby2ruby-1.2.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name ruby2ruby


Summary: Generate pure ruby from RubyParser compatible Sexps
Name: rubygem-%{gem_name}
Version: 2.1.1
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://seattlerb.rubyforge.org/ruby2ruby/
Source0: http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
# These test cases are carried in the ParseTree gem in test/. Carry them here
# rather than attempting to install ParseTree-doc in check and introducing a circular
# dependency
Source1: pt_testcase.rb
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: rubygems-devel
BuildRequires: ruby(release)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(sexp_processor)
BuildRequires: rubygem(ruby_parser)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
ruby2ruby provides a means of generating pure ruby code easily from
RubyParser compatible Sexps. This makes making dynamic language
processors in ruby easier than ever!

%package doc
Summary: Documentation for %{name}
Group: Documentation

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

cp -p %{SOURCE1} $(pwd)/%{gem_instdir}/test/

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/%{_bindir}
mv .%{_bindir}/* %{buildroot}/%{_bindir}
find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Drop the standalone mode for tests - won't run that way due to missing 
# rubygems require anyway.
find %{buildroot}%{gem_instdir}/test -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/.*\/ruby.*/d'
find %{buildroot}%{gem_libdir} -type f | \
  xargs -n 1 sed -i  -e '/^#!\/usr\/bin\/env.*/d'
# Ships with extremely tight permissions, bring them inline with other gems
find %{buildroot}%{gem_instdir} -type f | \
  xargs chmod 0644
find %{buildroot}%{gem_instdir}/bin -type f | \
  xargs chmod 0755

%check
pushd .%{gem_instdir}
ruby -Ilib:test test/test_ruby2ruby.rb
popd

%files
%defattr(-,root,root,-)
%{_bindir}/r2r_show
%doc %{gem_instdir}/History.txt
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.txt
%dir %{gem_instdir}
%{gem_instdir}/bin
%{gem_libdir}
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-,root,root,-)
%{gem_instdir}/Rakefile
%{gem_instdir}/.autotest
%{gem_instdir}/.gemtest
%{gem_instdir}/test
%{gem_docdir}

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Mo Morsi <mmorsi@redhat.com> - 2.1.1-1
- Update to 2.1.1
- fix build against rawhide (use latest pt_testcase.rb from sexp_processor)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Mo Morsi <mmorsi@redhat.com> - 2.0.6-1
- New upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.1-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Mo Morsi <mmorsi@redhat.com> - 2.0.1-2
- Add missing file

* Fri Nov 30 2012 Mo Morsi <mmorsi@redhat.com> - 2.0.1-1
- Update to new upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.4-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Mo Morsi <mmorsi@redhat.com> - 1.2.4-4
- replace BR(check) w/ BR

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 29 2009 Matthew Kent <mkent@magoazul.com> - 1.2.4-2
- Move pt_testcase.rb to the build stage so it's included in the rpm (#541512).
- Drop version requirements for sexp_processor and ruby_parser as they are new
  packages (#541512).

* Mon Nov 16 2009 Matthew Kent <mkent@magoazul.com> - 1.2.4-1
- Initial package
