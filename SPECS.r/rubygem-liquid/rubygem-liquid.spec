%global gem_name liquid

Name: rubygem-%{gem_name}
Version: 3.0.1
Release: 4%{?dist}
Summary: A secure, non-evaling end user template engine with aesthetic markup
Group: Development/Languages
License: MIT and Ruby
URL: http://www.liquidmarkup.org
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
%if 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
# rubygem-spy is not yet available in Fedora.
#BuildRequires: rubygem(spy)
BuildArch: noarch
%if 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Liquid is a template engine which was written with very specific requirements:
* It has to have beautiful and simple markup. Template engines which don't
  produce good looking markup are no fun to use.
* It needs to be non evaling and secure. Liquid templates are made so that
  users can edit them. You don't want to run code on your server which your
  users wrote.
* It has to be stateless. Compile and render steps have to be separate so that
  the expensive parsing and compiling can be done once and later on you can
  just render it passing in a hash with local variables and objects.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  # rubygem-spy is not yet available in Fedora.
  # Add a dummy "spy/integration" until the real package is available.
  mkdir spy
  touch spy/integration.rb
  # Run the tests, excluding the ones that require a real spy library
  ruby -I"lib:.:test" -e 'Dir.glob("./test/**/*_test.rb").each{|f| require f unless /context_unit_test/ =~ f }'
  # Clean up the dummy spy lib
  rm -r spy
popd


%files
%{!?_licensedir:%global license %%doc}
%dir %{gem_instdir}
%license %{gem_instdir}/MIT-LICENSE
%doc %{gem_instdir}/README.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/History.md
%exclude %{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 3.0.1-4
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.0.1-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.1-1
- Update to latest upstream release (RHBZ #1186292)

* Wed Jan 07 2015 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.0-2
- Add "Ruby" to License tag (RHBZ #1038274)
- Create a dummy "spy/integration" lib so we can run the tests during %%check
  (RHBZ #1038274)

* Wed Dec 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 3.0.0-1
- Update to latest upstream release
- Adjustments for https://fedoraproject.org/wiki/Changes/Ruby_2.1
- Use %%license tag
- Unconditionally pass tests until rubygem-spy is available

* Wed Dec 04 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 2.6.0-1
- Initial package
