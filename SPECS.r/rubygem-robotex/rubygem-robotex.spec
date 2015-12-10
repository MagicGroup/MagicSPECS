%global gem_name robotex

%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

%if 0%{?rhel} == 6 || 0%{?fedora} < 17
%define rubyabi 1.8
%else
%define rubyabi 1.9.1
%endif

Summary:    Ruby library to obey robots.txt 
Name:       rubygem-%{gem_name}
Version:    1.0.0
Release:    17%{?dist}
License:    MIT 
Group:      Development/Languages
URL:        http://www.github.com/chriskite/robotex
Source:     http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
Requires:   rubygems
%if 0%{?fedora} > 18
Requires:   ruby(release)
%else
Requires:   ruby(abi) = %{rubyabi}
%endif
Provides:   rubygem(%{gem_name}) = %{version}
BuildRequires:  rubygem(fakeweb)
BuildRequires:  rubygems
%if 0%{?fedora}
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
%endif
BuildArch:  noarch

%description
With one line of code, Robotex (pronounced like “robotics”) will download
and parse the robots.txt file and let you know if your program is allowed
to visit a given link.

%package doc
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
gem build %{gem_name}.gemspec

%build
%if 0%{?fedora} > 18
%gem_install
%else
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --force --rdoc %{gem_name}-%{version}.gem
%endif

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
%{__rm} -Rf %{buildroot}/%{gem_instdir}/.yardoc

%check
pushd .%{gem_instdir}
# remove requires of bundler/setup
sed -i 2d spec/spec_helper.rb
%if 0%{?fedora}
rspec spec/
%endif
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/VERSION

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/spec/

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.0.0-17
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.0-16
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.0-15
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.0-12
- use correct path (msuchy@redhat.com)

* Mon Mar 18 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.0-11
- do not require bundler (msuchy@redhat.com)

* Mon Mar 18 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.0-10
- run tests (msuchy@redhat.com)

* Fri Mar 15 2013 Miroslav Suchý <msuchy@redhat.com> 1.0.0-9
- comply to Fedora Guidelines (msuchy@redhat.com)

* Tue Jan 29 2013 Justin Sherrill <jsherril@redhat.com> 1.0.0-8
- dropping abi requires for robotex & anemone (jsherril@redhat.com)

* Tue Jan 22 2013 Justin Sherrill <jsherril@redhat.com> 1.0.0-7
- fixing robotext abi requires (jsherril@redhat.com)

* Tue Jan 22 2013 Justin Sherrill <jsherril@redhat.com> 1.0.0-6
- bumping version for build 

* Tue Jan 22 2013 Justin Sherrill <jsherril@redhat.com> 1.0.0-5
- fixing robotex build for rhel6 (jsherril@redhat.com)

* Fri Nov 30 2012 Justin Sherrill <jsherril@redhat.com> 1.0.0-4
- only require rubygems-devel on rhel 6 (jsherril@redhat.com)

* Fri Nov 30 2012 Justin Sherrill <jsherril@redhat.com> 1.0.0-3
- removing uneeded rm to fix build (jsherril@redhat.com)

* Fri Nov 30 2012 Justin Sherrill <jsherril@redhat.com> 1.0.0-2
- new package built with tito


* Mon Jul 16 2012 Justin Sherrill <jsherril@redhat.com>  0.7.2-1
- new package built with tito

