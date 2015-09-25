%global gem_name webrat

Summary: Ruby Acceptance Testing for Web applications
Name: rubygem-%{gem_name}
Version: 0.7.3
Release: 10%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/brynary/webrat
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(nokogiri)
Requires: rubygem(rack) >= 1.0
Requires: rubygem(rack-test)
BuildRequires: rubygems-devel
BuildRequires: rubygem(thor)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Webrat lets you quickly write expressive and robust acceptance tests
for a Ruby web application. It supports simulating a browser inside
a Ruby process to avoid the performance hit and browser dependency of
Selenium or Watir, but the same API can also be used to drive real
Selenium tests when necessary (eg. for testing AJAX interactions).

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# Remove vendored Selenium server
rm -rf %{buildroot}%{gem_instdir}/vendor

# Remove dot files
rm -rf %{buildroot}%{gem_instdir}/webrat.log
rm -rf %{buildroot}%{gem_instdir}/.document
find %{buildroot} -iname .gitignore -exec rm -f {} \;

# Fix shebang
chmod -x %{buildroot}%{gem_libdir}/webrat/core/configuration.rb
chmod -x %{buildroot}%{gem_instdir}/spec/private/core/configuration_spec.rb
chmod -x %{buildroot}%{gem_instdir}/spec/private/core/link_spec.rb
chmod +x %{buildroot}%{gem_instdir}/spec/integration/merb/tasks/merb.thor/app_script.rb

# the selenium server is large.  Despite the fact that we remove it above,
# it lives on inside of the original gem in the cache directory.  To reduce the
# size of the binary RPM, here we rebuild the gem itself and install it
rm -f %{buildroot}%{gem_cache}
mkdir -p .gemrebuild
pushd .gemrebuild
gem unpack %{SOURCE0}
pushd %{gem_name}-%{version}
sed -i '/\"vendor/d' webrat.gemspec
thor :build
cp pkg/%{gem_name}-%{version}.gem %{buildroot}%{gem_dir}/cache
popd
popd
rm -rf .gemrebuild


%files
%dir %gem_instdir
%gem_instdir/lib
%gem_instdir/install.rb
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/MIT-LICENSE.txt
%doc %{gem_instdir}/History.txt
%{gem_cache}
%{gem_spec}

%files doc
%defattr(-, root, root, -)
%gem_instdir/spec
%gem_instdir/Rakefile
%gem_instdir/Thorfile
%gem_instdir/Gemfile
%gem_instdir/%{gem_name}.gemspec
%{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.3-10
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 0.7.3-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.3-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Chris Lalancette <clalance@redhat.com> - 0.7.3-1
- Update to webrat 0.7.3

* Wed Oct 20 2010 Michal Fojtik <mfojtik@redhat.com> - 0.7.1-2
- Initial package
