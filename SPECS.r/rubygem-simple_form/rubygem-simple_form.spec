%global gem_name simple_form

%global mainver 3.1.0
%global prever .rc
%global prerelease 2
%{?prever:
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{mainver}%{?prever}%{?prerelease}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{mainver}%{?prever}%{?prerelease}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{mainver}%{?prever}%{?prerelease}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{mainver}%{?prever}%{?prerelease}.gemspec
}

Name: rubygem-%{gem_name}
Version: %{mainver}
Release: %{?prever:0.}2%{?prever}%{?prerelease}%{?dist}.1
Summary: Flexible and powerful components to create forms

Group: Development/Languages
License: MIT
URL: https://github.com/plataformatec/%{gem_name}
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}%{?prever}%{?prerelease}.gem

Provides: rubygem(%{gem_name}) = %{version}
BuildArch: noarch
BuildRequires: rubygems-devel
# Test suite needs the following dependencies
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(minitest) >= 5.0
BuildRequires: rubygem(railties)
BuildRequires: rubygem(activemodel)
BuildRequires: rubygem(tzinfo)


%description
SimpleForm aims to be as flexible as possible while helping you with powerful
components to create your forms. The basic goal of SimpleForm is to not touch
your way of defining the layout, letting you find the better design for your
eyes.


%package doc
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Summary: Documentation for %{name}


%description doc
This package contains documentation %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}%{?prever}%{?prerelease}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec


%build

# Create the gem as gem install only works on a gem file
LANG=en_US.utf8 gem build %{gem_name}.gemspec

# gem install compiles any C extensions and installs into a directory
# We set that to be a local directory so that we can move it into the
# buildroot in %%install
%gem_install -n %{SOURCE0}


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/


%check
pushd ./%{gem_instdir}
# Get rid of Bundler.
sed -i "/require 'bundler\/setup'/d" test/test_helper.rb
# The following test cases require rubygem-country_select which is not packaged
# for Fedora, so commenting it out
sed -i "/require 'country_select'/d" test/test_helper.rb
sed -i '121,124 s|^|#|' test/form_builder/general_test.rb
sed -i '5,17 s|^|#|' test/inputs/priority_input_test.rb
sed -i '38,48 s|^|#|' test/inputs/priority_input_test.rb
ruby -Ilib:test -e 'Dir.glob "./test/*_test.rb", &method(:require)'
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%doc %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.md
%exclude %{gem_cache}
%{gem_spec}


%files doc
%{gem_instdir}/test
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.1.0-0.2.rc2.1
- 为 Magic 3.0 重建

* Wed Oct 08 2014 Josef Stribny <jstribny@redhat.com> - 3.1.0-0.1.rc2
- Update to 3.1.0.rc2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-0.2.rc.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 19 2013 Josef Stribny <jstribny@redhat.com> - 3.0.0-0.1.rc
- Update to simple_form 3.0.0.rc

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 21 2012 Imre Farkas <ifarkas@redhat.com> - 2.0.3-1
- Initial package
