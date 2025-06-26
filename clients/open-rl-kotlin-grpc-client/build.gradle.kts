import com.google.protobuf.gradle.id

dependencies {
    implementation("com.google.protobuf:protobuf-java:4.28.2")
    implementation("io.grpc:grpc-protobuf:1.60.0")
    implementation("io.grpc:grpc-stub:1.60.0")
    implementation("io.grpc:grpc-kotlin-stub:1.4.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    runtimeOnly("io.grpc:grpc-netty:1.60.0")
}

protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:3.24.0" // Protobuf compiler
    }
    plugins {
        id("grpc") {
            artifact = "io.grpc:protoc-gen-grpc-java:1.60.0"
        }
        id("grpc-kotlin") {
            artifact = "io.grpc:protoc-gen-grpc-kotlin:1.4.1:jdk8@jar"
        }
    }
    generateProtoTasks {
        all().forEach {
            it.plugins {
                id("grpc")
                id("grpc-kotlin")
            }
        }
    }
}

sourceSets {
    main {
        proto {
            srcDir("${rootDir}/protos") // Location of .proto files
        }
    }
}

tasks.named("build") {
    dependsOn("generateProto")
}
