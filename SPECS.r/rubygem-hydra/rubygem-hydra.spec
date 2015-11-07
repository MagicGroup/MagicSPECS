%global gem_name hydra
%global rubyabi 1.9.1

%if 0%{?el6}%{?fc16}
%global rubyabi 1.8
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%global gem_libdir %{gem_instdir}/lib
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%endif

Summary: Distributed testing toolkit
Name: rubygem-%{gem_name}
Version: 0.24.0
Release: 8%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/ngauthier/hydra
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fedora} >= 19
Requires: ruby(release)
%else
Requires: ruby(abi) = %{rubyabi}
%endif
Requires: rubygems
Requires: rubygem(shoulda)

%if 0%{?el6}%{?fc16}
BuildRequires: rubygems
%else
BuildRequires: rubygems-devel
%endif

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}



%description
Spread your tests over multiple machines to test your code faster.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep

%build

%install
rm -rf %{buildroot}
%if 0%{?fedora}
%gem_install -n %{SOURCE0} -d %{buildroot}%{gem_dir}
%else
mkdir -p %{buildroot}%{gem_dir}
gem install --local --install-dir %{buildroot}%{gem_dir} \
            --force --rdoc %{SOURCE0}
%endif

# Remove unnecessary file
rm %{buildroot}%{gem_instdir}/.document

chmod 755 %{buildroot}%{gem_instdir}/test/fixtures/hello_world.rb
chmod 755 %{buildroot}%{gem_instdir}/test/fixtures/many_outputs_to_console.rb

%check

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/caliper.yml
%{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/VERSION
%doc %{gem_instdir}/README.rdoc

%files doc
%{gem_instdir}/hydra-icon-64x64.png
%{gem_instdir}/hydra_gray.png
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}
%doc %{gem_instdir}/TODO


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.24.0-8
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.24.0-7
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Josef Stribny <jstribny@redhat.com> - 0.24.0-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 10 2012 Matt Hicks <mhicks@redhat.com> - 0.24.0-1
- Initial package
