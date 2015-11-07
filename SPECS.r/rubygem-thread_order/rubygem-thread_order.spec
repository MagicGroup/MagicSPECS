%global	gem_name	thread_order

Name:		rubygem-%{gem_name}
Version:	1.1.0
Release:	3%{?dist}

Summary:	Test helper for ordering threaded code
License:	MIT
URL:		https://github.com/JoshCheek/thread_order
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
BuildRequires:	rubygem(rspec) >= 3
BuildArch:	noarch

%description
Test helper for ordering threaded code.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

pushd %{buildroot}
rm -f .%{gem_cache}

pushd .%{gem_instdir}
rm -rf \
	.gitignore .travis.yml \
	Gemfile \
	spec/ \
	%{gem_name}.gemspec \
	%{nil}

popd
popd

%check
# The following test does not pass with using gem
FAILFILE=()
FAILTEST=()
FAILFILE+=("spec/thread_order_spec.rb")
FAILTEST+=("is implemented without depending on the stdlib")

pushd .%{gem_instdir}
for ((i = 0; i < ${#FAILFILE[@]}; i++)) {
	sed -i \
		-e "\@${FAILTEST[$i]}@s|do$|, :broken => true do|" \
		${FAILFILE[$i]}
}

rspec spec/ || \
	rspec spec/ --tag ~broken
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/License.txt
%doc	%{gem_instdir}/Readme.md

%{gem_libdir}
%{gem_spec}

%files doc
%doc	%{gem_docdir}

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.1.0-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.1.0-2
- 为 Magic 3.0 重建

* Sun Aug 09 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- Initial package
