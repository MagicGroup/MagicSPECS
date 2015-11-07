%global gem_name wikicloth

Name: rubygem-%{gem_name}
Version: 0.8.0
Release: 6%{?dist}
Summary: Mediawiki parser
Group: Development/Languages
License: MIT
URL: https://github.com/nricciar/wikicloth
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Minitest 5 support
# https://github.com/nricciar/wikicloth/pull/69
Patch0: rubygem-wikicloth-0.8.0-minitest.patch
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: rubygem(builder)
Requires: rubygem(expression_parser)
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(expression_parser)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
An implementation of the mediawiki markup in Ruby.


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

# Minitest 5 support
# https://github.com/nricciar/wikicloth/pull/69
%patch0 -p1

# Remove developer-only files.
for f in .gitignore .travis.yml Gemfile Rakefile run_tests.rb tasks/wikicloth_tasks.rake; do
  rm $f
  sed -i "s|\"$f\",||g" %{gem_name}.gemspec
done

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install

# Remove unnecessary gemspec
rm .%{gem_instdir}/%{gem_name}.gemspec

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
  ruby -Ilib test/*_test.rb
popd


%files
%dir %{gem_instdir}
%doc %{gem_instdir}/README
%doc %{gem_instdir}/README.textile
%doc %{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%{gem_instdir}/init.rb
%{gem_instdir}/lang

%files doc
%doc %{gem_docdir}
%exclude %{gem_instdir}/test
%{gem_instdir}/examples
%{gem_instdir}/sample_documents

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.8.0-6
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.8.0-5
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 10 2014 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.0-3
- Patch for Minitest 5 (RHBZ #1107264)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 06 2013 Ken Dreyer <ktdreyer@ktdreyer.com> - 0.8.0-1
- Initial package
