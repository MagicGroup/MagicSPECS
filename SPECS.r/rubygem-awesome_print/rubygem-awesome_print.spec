# Generated from awesome_print-1.0.2.gem by gem2rpm -*- rpm-spec -*-
%global gem_name awesome_print

Summary: Pretty print Ruby objects with proper indentation and colors
Name: rubygem-%{gem_name}
Version: 1.0.2
Release: 11%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/michaeldv/awesome_print
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ruby
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem-rspec
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Great Ruby debugging companion: pretty print Ruby objects to visualize their
structure. Supports custom object formatting via plugins.


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

# not running tests since it's broken in mock
#%check
#pushd ./%{gem_instdir}
#rspec -Ilib spec/
#popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
echo %{gem_dir}
echo %{buildroot}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
rm %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/.gitignore
rm %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/Gemfile.lock
chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/lib/awesome_print/formatter.rb
chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/lib/ap.rb
chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/lib/awesome_print/inspector.rb
chmod -x %{buildroot}%{gem_dir}/gems/%{gem_name}-%{version}/lib/awesome_print.rb


%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%{gem_instdir}/LICENSE
%{gem_instdir}/Gemfile

%files doc
%doc %{gem_docdir}
%{gem_instdir}/LICENSE
%{gem_instdir}/CHANGELOG
%{gem_instdir}/README.md
%{gem_instdir}/spec/
%{gem_instdir}/spec/colors_spec.rb
%{gem_instdir}/spec/formats_spec.rb
%{gem_instdir}/spec/methods_spec.rb
%{gem_instdir}/spec/objects_spec.rb
%{gem_instdir}/spec/spec_helper.rb
%{gem_instdir}/Rakefile

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.2-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012  <mzatko@redhat.com> - 1.0.2-6
- Owning spec directory

* Thu Oct 04 2012  <mzatko@redhat.com> - 1.0.2-5
- Moved specs into docs, using rm instead of exclude
- Not removing Gemfile

* Thu Sep 20 2012  <mzatko@redhat.com> - 1.0.2-4
- Renamed spec file to rubygem_awesome_print.spec

* Tue Sep 04 2012  <mzatko@redhat.com> - 1.0.2-3
- Added license file to doc, files in doc use docdir instead of instdir

* Mon Sep 03 2012  <mzatko@redhat.com> - 1.0.2-2
- Removed unnecessary files & corrected license

* Wed Jul 11 2012  <mzatko@redhat.com> - 1.0.2-1
- Initial package
